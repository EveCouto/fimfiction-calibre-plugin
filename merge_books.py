
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime


def merge_opf(opf1: bytes, opf2: bytes) -> bytes:
    """Takes 2 opf files and combines their data

    Args:
        opf1 (bytes): opf1 file contents
        opf2 (bytes): opf2 file contents

    Returns:
        bytes: combined opf file contents
    """

    # Setting up XML parsing
    NS = {"opf": "http://www.idpf.org/2007/opf"}
    ET.register_namespace("", NS["opf"])
    ET.register_namespace("dc", "http://purl.org/dc/elements/1.1/")

    # Initializess the XMLs
    root1 = ET.fromstring(opf1)
    root2 = ET.fromstring(opf2)

    # Merge opf manifests
    manifest1 = root1.find("opf:manifest", NS)
    manifest2 = root2.find("opf:manifest", NS)

    seen = {item.get("id") for item in manifest1}

    for item in manifest2:
        if item.get("id") not in seen:
            manifest1.append(item)
            seen.add(item.get("id"))

    # Merge opf spines
    spine1 = root1.find("opf:spine", NS)
    spine2 = root2.find("opf:spine", NS)

    seen = {item.get("idref") for item in spine1}

    for item in spine2:
        if item.get("idref") not in seen:
            spine1.append(item)
            seen.add(item.get("idref"))

    # Returns the merged opf
    return ET.tostring(root1, encoding="utf-8", xml_declaration=True)


def merge_epub(old_path: str, new_path: str, out_path: str):
    """Takes 2 epub files, outputs the combined epub

    Args:
        old_path (str): original epub path
        new_path (str): updated epub path
        out_path (str): output path
    """

    # Sets all files to be opened
    with (zipfile.ZipFile(old_path) as old_zip,
          zipfile.ZipFile(new_path) as new_zip,
          zipfile.ZipFile(out_path, "w") as out_zip):

        # Adds old epub files to temp epub
        for old_zip_info in old_zip.infolist():
            with old_zip.open(old_zip_info) as in_file:
                content = in_file.read()
            if ".opf" in old_zip_info.filename:
                old_opf = content
            # Skips config files where new version is needed
            elif ("toc.html" not in old_zip_info.filename and
                  ".ncx" not in old_zip_info.filename):
                out_zip.writestr(old_zip_info.filename, content)

        # Adds files not already added to the temp epub
        current_files = out_zip.namelist()
        for new_zip_info in new_zip.infolist():
            if new_zip_info.filename not in current_files:
                with new_zip.open(new_zip_info) as in_file:
                    content = in_file.read()
                if ".opf" in new_zip_info.filename:
                    new_opf = content
                else:
                    out_zip.writestr(new_zip_info.filename, content)

        # Adds the opf file to the temp epub
        merged_opf = merge_opf(old_opf, new_opf)
        out_zip.writestr("book.opf", merged_opf)


def merge_books(temp_dir: str, original_book_path: str, merge_book_path: str,
                backup: bool, backup_path: str) -> str:
    """Merges books and saves a copy to backup folder.

    Args:
        temp_dir (str): temporary directory where file edits will be made
        original_book_path (str): old / original version of epub
        merge_book_path (str): new version of epub
        backup (bool): if backups will be done
        backup_path (str): backup path

    Returns:
        str: file path where the merged epub is
    """
    # Temp path is where the merged epub will be.
    temp_file = "temp.epub"
    temp_path = os.path.join(temp_dir, temp_file)

    # Merges the files into temp_path
    merge_epub(original_book_path, merge_book_path, temp_path)

    # Do backups here: TODO
    if backup:
        now = datetime.now().strftime(r"%Y-%m-%d-%H-%M-%S")
        safe_loc = os.path.join(
            backup_path, os.path.basename(original_book_path))
        safe_loc = safe_loc.replace(".epub", "")
        safe_loc = safe_loc + "-" + now + "-bk.epub"
        shutil.copy2(original_book_path, safe_loc)

    return temp_path
