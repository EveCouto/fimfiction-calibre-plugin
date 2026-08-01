import os
import zipfile
import re
import urllib.parse
import urllib.request
import shutil
from datetime import datetime


def scan_zip(zip_path: str, file_ext: str,
             pattern: str = r"(<img src=\"http[^>]*\/>)", ) -> dict:
    """Scans zip file for pattern matches in files

    Args:
        zip_path (str): filepath of zip
        pattern (str): regex pattern, defaults
        file_ext (str): file extension

    Returns:
        dict: filename -> match(es)
    """

    loc_to_match = {}

    # Open zip, read files and gets instances of pattern
    with zipfile.ZipFile(zip_path) as zip:
        for zip_info in zip.infolist():
            if file_ext in zip_info.filename:
                with zip.open(zip_info) as in_file:
                    content = in_file.read().decode()
                    matches = re.findall(pattern, content)
                    if matches:
                        loc_to_match[zip_info.filename] = matches
    return loc_to_match


def hidden_link_fix(link: str, pattern: str = r'url=(.*?)(?=%3F|")') -> str:
    """checks string and extracts hidden url

    Args:
        link (str): a string containing a hidden link
        pattern (str): regex pattern. Optional. Defaults to r"url=(.*)\"".

    Returns:
        str: fixed link or original if no changes
    """

    # Checks for matches in link
    matches = re.search(pattern, link)

    # Returns unquoted version if a match
    if matches:
        return urllib.parse.unquote(matches.group(1))
    else:
        if link.find("?"):
            return link[link.find("http"):link.find("?")]
        else:
            return link[link.find("http"):link.find('"')]


def get_img_data(img: str) -> dict:
    """Takes string and gets more info out of it

    Args:
        img (str): string representing an img url

    Returns:
        dict: contains all the img info
    """

    img_link = hidden_link_fix(img)
    img_name = os.path.basename(img_link)
    new_src = f'<img src="images/{img_name}"/>'

    return {"orig": img, "link": img_link,
            "name": img_name, "src": new_src}


# TODO maybe use proper xml parsing later...
def update_xml(xml: str, links: set):
    """Updates XML, only really works with byte

    Args:
        xml (str): xml text
        links (set): links used in update

    Returns:
        byte: xml text output
    """

    upper = xml[:xml.find(bytes("</manifest>", "cp437"))]
    lower = xml[xml.find(bytes("</manifest>", "cp437")):]

    for link in links:
        name = os.path.basename(link)
        if bytes(name, "cp437") not in xml:
            media = os.path.splitext(name)[1]
            add = (f'\t<item id="{name}" ' +
                   f'href="images/{name}" ' +
                   f'media-type="image/{media}" />\n\t')
            upper += bytes(add, "cp437")

    return upper + lower


def request_image(link: str, log=None):
    """tries to request an image from internet

    Args:
        link (str): link trying to retrieve
        log (_type_, optional): log for calibre. Defaults to None.

    Returns:
        str: the content of file or None
    """
    try:
        if log:
            log(" " * 5, f"Downloading: '{link}'")
        # Tries to get the data from the link
        file = urllib.request.urlopen(link, timeout=20).read()
    except urllib.error.HTTPError:
        if log:
            log("\t**Download Failed, HTTP Error**")
        return None
    except TimeoutError:
        # Allows for one timeout before assuming broken link
        try:
            file = urllib.request.urlopen(link, timeout=20).read()
        except TimeoutError:
            if log:
                log(" " * 10, "**Download Failed, Timed Out**")
            return None
    return file


def update_zip(in_zip_path: str, out_zip_path: str,
               file_to_img: dict[str, list[str]],
               log=None) -> str:
    """Takes input and output and data to update epub zip

    Args:
        in_zip_path (str): input filepath
        out_zip_path (str): output filepath
        file_to_img (dict[str, list[str]]): data dict
    Return:
        str: path of fixed file
    """

    # Updates data in dictionary
    for key in file_to_img.keys():
        file_to_img[key] = list(map(get_img_data, file_to_img[key]))

    # Gets all links into a set to prevent duplicates
    links = set()
    successful_links = set()
    for key in file_to_img.keys():
        for img in file_to_img[key]:
            links.add(img["link"])

    if len(links) == 0:
        if log:
            log(" " * 5, "**No Images to fix, skipping**")
        return ""

    opf_file = ""

    # Opens input and output zip files.
    with (zipfile.ZipFile(in_zip_path) as in_zip,
          zipfile.ZipFile(out_zip_path, 'w') as out_zip):
        all_in_files = set(in_zip.namelist())
        for in_zip_info in in_zip.infolist():
            with in_zip.open(in_zip_info) as in_file:
                content = in_file.read()

            # Runs through all documents needing editing and updates
            if in_zip_info.filename in file_to_img.keys():
                for img in file_to_img[in_zip_info.filename]:
                    # Sets cleaner variable names
                    link = img["link"]
                    name = os.path.basename(link)

                    # updates the html link to point at file
                    content = content.replace(
                        bytes(img["orig"], "cp437"),
                        bytes(img["src"], "cp437"))

                    # Ensures no files will be duplicated
                    if link in links and name not in all_in_files:
                        # Gets image and writes the data to the zip
                        if img_bytes := request_image(link, log):
                            out_zip.writestr(f"{"images/" + name}", img_bytes)
                            links.discard(link)
                            successful_links.add(link)
                        else:
                            # If getting image fails, content is updated
                            # To reflect this
                            html_string = ("<a class='failed-img' " +
                                           "rel='nofollow' " +
                                           f"href='{link}'>" +
                                           " Image request failed: " +
                                           "Click to try and view </a>")
                            content = content.replace(
                                bytes(img["src"], "cp437"),
                                bytes(html_string, "cp437"))

            # Runs through the opf data file
            if ".opf" in in_zip_info.filename:
                opf_file = in_zip_info.filename

            out_zip.writestr(in_zip_info.filename, content)

        if opf_file:
            with in_zip.open(opf_file) as in_file:
                content = in_file.read()
                content = update_xml(content, successful_links)
                out_zip.writestr(opf_file, content)

    return out_zip_path


def fix_images(temp_dir: str, book_path: str,
               backup: bool = False, backup_path: str = None,
               retry: bool = False, log=None) -> str:
    """Takes a dir, a book and backup info and fixes images

    Args:
        temp_dir (str): directory where files will be edited
        book_path (str): path to an epub
        backup (bool): if backups occur
        backup_path (str): backup path

    Returns:
        str: returns the file path for the fixed book
    """
    # Temp path is where the fixed epub will be
    temp_file = os.path.basename(book_path)
    temp_path = os.path.join(temp_dir, "temp-" + temp_file)
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Actually updates the book
    fixed_path = update_zip(
        book_path, temp_path, scan_zip(book_path, ".html"), log)

    # Backups
    if backup and fixed_path:
        now = datetime.now().strftime(r"%Y-%m-%d-%H-%M-%S")
        safe_loc = os.path.join(
            backup_path, os.path.basename(book_path))
        safe_loc = safe_loc.replace(".epub", "")
        safe_loc = safe_loc + "-" + now + "-bk.epub"
        shutil.copy2(book_path, safe_loc)

    if fixed_path:
        return fixed_path
    else:
        return ""
