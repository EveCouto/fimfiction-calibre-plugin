# fimfiction-calibre-plugin

Allows for retrieving images and inserting into epubs as well as merging epubs to update them.

## Usage

Download the Zip and install the zip plugin in Calibre

Manually add the 'FimFic Merge/Fix' tool to the toolbar

The main button is set to Merge.

The dropdown, has merge, fix images and, config plugin.


### Config Plugin

Config plugin contains the ability to turn on backing up the files, must select the box and then choose a directory by clicking the button below

Any edits made using this plugin will be backed up to the designated folder. This is strongly recommended as there may be issues.

### Merge

Select one book in the Calibre library, then when the button is clicked a file dialog will appear

Now select the new updated version of the epub, ie old version has 10 chapters and new version has 20

The plugin will then merge the files giving priority to the original, so it will only add chapters but, not edit the older chapters

It's primary use is not overriding the images added in the next section

### Fix Images

Select 1 or more books (in epub format) in your Calibre Library then click the Fix Images Button

It will then send then to the jobs tab in the bottom right

Each book will then be scanned for images and if the image is a link it will attempt to download it

Once downloaded it will be inserted into the book's files

It is not perfect and if it fails to download the reference in the epub will still be changed so it will not try it again on a second attempt
