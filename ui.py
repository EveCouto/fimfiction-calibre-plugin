from calibre.gui2.actions import InterfaceAction
from qt.core import QMenu


class InterfacePlugin(InterfaceAction):
    name = "Fimfiction Ebook Plugin"

    action_spec = ('FimFic Merge/Fix',
                   None,
                   'Merge Selected Book',
                   None)

    def genesis(self):
        """Sets up the UI elements in Calibre"""
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
            triggered=self.start_image_fix
        )

        # Sub menu item 2
        self.create_menu_action(
            self.menu,
            unique_name="merge_books",
            text="Merge Books",
            triggered=self.open_book_merge
        )

        # Sub menu item 3
        self.create_menu_action(
            self.menu,
            unique_name="config_plugin",
            text="Config Plugin",
            triggered=self.open_config
        )

    def start_image_fix(self):
        """Starts the image fix job"""

        # Imports
        from calibre.gui2.threaded_jobs import ThreadedJob
        from calibre.gui2 import error_dialog

        # Get selected books in library
        rows = self.gui.library_view.selectionModel().selectedRows()

        # Ensures items selected in Calibre
        if not rows:
            return error_dialog(
                self.gui, 'Error', 'Nothing Selected', show=True)

        # List of Calibre IDs used in the actual job
        book_ids = list(map(self.gui.library_view.model().id, rows))

        # Creates the job object
        job = ThreadedJob(
            "fimfic_fix_fix_images",
            "Fixing images",
            self.run_image_fix,
            (book_ids,),
            {},
            self.image_fix_finished
        )

        # Runs the job
        self.gui.job_manager.run_threaded_job(job)

    def run_image_fix(self, book_ids: list[str],
                      log=None, notifications=None, abort=None):
        """Runs the actual image fix code

        Args:
            book_ids (list[str]): a list of calibre book ids
            log (_type_, optional): calibre log. Defaults to None.
            notifiations (_type_, optional): calibre notifications.
                Defaults to None.
        """

        # Imports
        import os
        from calibre_plugins.fimfic_fix.fix_images import fix_images
        from calibre.ptempfile import TemporaryDirectory
        from calibre_plugins.fimfic_fix.config import prefs

        # Gets the database from Calibre
        db = self.gui.current_db.new_api

        # uses a temp directory to work in.
        with TemporaryDirectory() as tdir:
            for index, book_id in enumerate(book_ids):
                epub_name = os.path.basename(
                    db.format_abspath(book_id, "EPUB"))

                # Notifications and log for Calibre
                if notifications:
                    notifications.put(
                        (float(index/len(book_ids)),
                         f"Fixing file {index+1} / {len(book_ids)}: " +
                         f"'{epub_name}'"))

                if log:
                    log("-" * 150)
                    log(f"Started file: '{epub_name}'")

                # Copies epub over to temp dir
                temp_epub = os.path.join(tdir, epub_name)
                db.copy_format_to(book_id, "EPUB", temp_epub)

                # fixes the book at temp dir, returning the new location
                fixed_epub = fix_images(
                    tdir, temp_epub,
                    prefs["do_backups"], prefs["backup_path"], log)

                # Copies the edit back into Calibre
                if fixed_epub:
                    db.add_format(book_id, "EPUB", fixed_epub, replace=True)
                    if log:
                        log(f"Completed file: '{epub_name}'")
                else:
                    if log:
                        log(f"File Unchanged: '{epub_name}'")

            # Completion Log
            if log:
                log("-" * 150)
                if prefs["do_backups"]:
                    log("Finished job: Fixing Images\n" +
                        f"Backups made at {prefs["backup_path"]}")
                else:
                    log("Finished job: Fixing Images")

        return

    def image_fix_finished(self, job):
        """Runs on completion or failure of the image_fix job

        Args:
            job (_type_): Calibre job object
        """

        # Import
        from calibre.gui2 import error_dialog

        # Catches for failure or canellation
        if job.failed:
            error_dialog(self.gui, "Fix Images Failed")
            return

        if job.abort:
            return

    def open_book_merge(self):
        """Runs the book merge functionality"""

        # Imports
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

        # Gets merge path, opens to download folder
        merge_path, _ = QFileDialog.getOpenFileName(
            self.gui,
            "Select EPUB",
            os.path.expanduser("~/Downloads"),
            "EPUB files (*.epub)")
        if not merge_path:
            return error_dialog(
                self.gui, 'Error', 'No File Selected', show=True)
        try:
            # Uses a temp directory to work in
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
        except Exception as e:
            return error_dialog(
                self.gui, 'Error', f'Error: {e}', show=True)

        if prefs["do_auto_fix"]:
            self.start_image_fix()

        # Simple dialog on completion
        dialog_str = (
            f"Book: '{mi.title}' has been merged with, '{merge_path}'.\n")
        if prefs["do_backups"]:
            dialog_str += f"\nBackup saved to '{prefs['backup_path']}'\n"
        if prefs["do_auto_fix"]:
            dialog_str += (f"\nFix Images ran on '{mi.title}', " +
                           "check jobs to see progress\n")

        info_dialog(self.gui, "Book Merged!", dialog_str, show=True)

    def open_config(self):
        """Config Running"""
        base_plugin_object = self.interface_action_base_plugin
        do_user_config = base_plugin_object.do_user_config
        do_user_config(self.gui)

    def apply_settings(self):
        """Setting Applying"""
        from calibre_plugins.fimfic_fix.config import prefs
        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        self.prefs = prefs
