# fimfiction-calibre-plugin

Allows for retrieving and inserting images into epubs as well as merging epubs to update them.

## Install and Setup

Download the Zip and install the zip plugin in Calibre.

Manually add the 'FimFic Merge/Fix' tool to the toolbar.

The main button is set to Merge by default.

The dropdown, has all available functions including the config.

## Config Plugin

Config plugin contains all the setting that the plugin currently supports.

All optional features are disabled by default and it is recommended to check it out on install.

### About Plugin

Shows this information in Calibre.

### Main Button Function

Allows for choosing what the main button in the Calibre UI does, supports all functions that the plugin has.

### Backup Files and Folder

Gvies the ability to turn on backing up the files, uses file explorer to choose a folder.

Any edits made using this plugin will be backed up to the designated folder. This is recommended as there may be issues.

\*Note: When using the Fix Images + Retry or Always retry is enabled, it will backup even if no changes made.\*

### Check Metadata on Merge Books

Will check the metadata, specifially the identifier (isbn or uri), title, and creator (author) of both epubs, if they are not identical it fails.

### Auto-run Fix Images on Merge Books

Will automatically run the Fix Images function after merging epubs.

### Always retry images on Fix Images

Every time the fix images is run, it will attempt to retry failed images.

\*Note: When ennabled, it will backup (if backup enabled) even if no changes made.\*

## Merge Books

Select one book in the Calibre library, when Merge is run a file dialog will appear.

Now select the new updated version of the epub, ie old version has 10 chapters and new version has 20.

The plugin will then merge the files giving priority to the original, so it will only add chapters but, not edit the older chapters.

It's primary use is not overriding the images added in the next section.

\*Note: If a book changes the order of chapters, merge will not work correctly.\*

Example of this is if a prequel chapter is added to the beginning of a book, it will not add them, but add duplicates of the most recent chapter.

## Merge Books Full

The same as Merge Books, but it prioritizes the new file. This fixes the issue mentioned in Merge Books.

It is left as its own function because of how it is run, Merge Books Full must run Fix Images automatically after a merge.

## Fix Images

Select 1 or more books (in epub format) in your Calibre Library then click the Fix Images button.

It will then send the process to the jobs tab in the bottom right.

Each book will then be scanned for images and if the image is a link it will attempt to download it.

Once downloaded it will be inserted into the book's files.

On failed downloads the link will be placed in the book if a reader wants to try and open it. The download feature fails on certain links due to it not being human presence.

## Fix Images + Retry

Does exactly the same as Fix Images, but will retry any failed images.

\*Note: When used, it will backup (if backup enabled) even if no changes made.\*
