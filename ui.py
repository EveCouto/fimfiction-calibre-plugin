from calibre.gui2.actions import InterfaceAction
from qt.core import QMenu


class InterfacePlugin(InterfaceAction):
    name = "Fimfiction Ebook Plugin"

    action_spec = ('FimFic Merge/Fix',
                   None,
                   'Merge Selected Book',
                   None)
    
    

    def genesis(self):
        # Icons
        icon = get_icons('images/icon.png', "Fimfiction Ebook Plugin")
        self.qaction.setIcon(icon)

        # Main Button Action
        self.qaction.triggered.connect(self.open_book_merge)

        # Sub menu
        self.menu = QMenu(self.gui)
        self.qaction.setMenu(self.menu)

        # Sub menu item 1
        self.create_menu_action(
            self.menu,
            unique_name="image_fix",
            text="Fix Images",
            triggered=self.open_image_fix
        )

        # Sub menu item 2
        self.create_menu_action(
            self.menu,
            unique_name="merge_books",
            text="Merge",
            triggered=self.open_book_merge
        )

        # Sub menu item 3
        self.create_menu_action(
            self.menu,
            unique_name="config_plugin",
            text="Config Plugin",
            triggered=self.open_config
        )

    def open_image_fix(self):
        from calibre_plugins.fimfic_fix.fix_images import fix_images
        from calibre.gui2 import info_dialog, error_dialog
        from calibre.ptempfile import TemporaryDirectory
        from calibre_plugins.fimfic_fix.config import prefs
        import os

        # Gets selected items in Calibre
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return error_dialog(
                self.gui, 'Error', 'Nothing Selected', show=True)

        book_ids = list(map(self.gui.library_view.model().id, rows))
        db = self.gui.current_db.new_api

        with TemporaryDirectory() as tdir:
            for book_id in book_ids:
                epub_path = db.format_abspath(book_id, "EPUB")
                filename = os.path.basename(epub_path)
                temp_epub = os.path.join(tdir, filename)
                db.copy_format_to(book_id, "EPUB", temp_epub)

                # Merges the books
                fixed_epub = fix_images(
                    tdir, temp_epub,
                    prefs["do_backups"], prefs["backup_path"])

                db.add_format(book_id, "EPUB", fixed_epub, replace=True)

        # Sets dialog string
        if prefs["do_backups"]:
            dialog_str = (
                f"{len(rows)} books have had their images fixed.\n\n" +
                f"Backups of the originals saved to '{prefs["backup_path"]}'" +
                "\n\nBooks Fixed:\n")
        else:
            dialog_str = (
                f"{len(rows)} books have fixed images.\n\nBooks fixed:\n")

        # Adds all the book titles to the dialog
        for book_id in book_ids:
            dialog_str += f"{db.get_metadata(book_id).title}\n"

        info_dialog(self.gui, "Images Fixed!", dialog_str, show=True)

    def open_book_merge(self):
        from calibre_plugins.fimfic_fix.merge_books import merge_books
        from calibre.gui2 import info_dialog, error_dialog
        from calibre.ptempfile import TemporaryDirectory
        from qt.core import QFileDialog
        from calibre_plugins.fimfic_fix.config import prefs
        import os

        # Gets selected items in Calibre
        rows = self.gui.library_view.selectionModel().selectedRows()
        # Ensures only 1 item is slected for merge
        if not rows or len(rows) == 0:
            return error_dialog(
                self.gui, 'Error', 'Nothing Selected', show=True)
        elif len(rows) >= 2:
            return error_dialog(
                self.gui, 'Error', 'More than 1 Book Selected', show=True)

        # Get info on selected item
        row = rows[0]
        book_id = self.gui.library_view.model().id(row)
        db = self.gui.current_db.new_api
        mi = db.get_metadata(book_id)

        # Gets merge path
        merge_path, _ = QFileDialog.getOpenFileName(
            self.gui, "Select EPUB", "", "EPUB files (*.epub)")
        if not merge_path:
            return error_dialog(
                self.gui, 'Error', 'No File Selected', show=True)

        with TemporaryDirectory() as tdir:
            epub_path = db.format_abspath(book_id, "EPUB")
            filename = os.path.basename(epub_path)
            temp_epub = os.path.join(tdir, filename)
            db.copy_format_to(book_id, "EPUB", temp_epub)

            # Merges the books
            merged_epub = merge_books(
                tdir, temp_epub, merge_path,
                prefs["do_backups"], prefs["backup_path"])

            db.add_format(book_id, "EPUB", merged_epub, replace=True)

        # Simple print TODO will remove later
        if prefs["do_backups"]:
            dialog_str = (
                f"Book: '{mi.title}' has been merged with, '{merge_path}'.\n" +
                f"\nBackup of the original saved to '{prefs["backup_path"]}'")
        else:
            dialog_str = (
                f"Book: '{mi.title}' has been merged with, '{merge_path}'.")

        info_dialog(self.gui, "Book Merged!", dialog_str, show=True)

    def open_config(self):
        base_plugin_object = self.interface_action_base_plugin
        do_user_config = base_plugin_object.do_user_config
        do_user_config(self.gui)

    def apply_settings(self):
        from calibre_plugins.fimfic_fix.config import prefs
        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        self.prefs = prefs
