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
            triggered=self.start_image_fix
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

    def start_image_fix(self):
        from calibre.gui2.threaded_jobs import ThreadedJob
        import tempfile
        from calibre_plugins.fimfic_fix.config import prefs

        # Get selected books in library
        rows = self.gui.library_view.selectionModel().selectedRows()

        if not rows:
            return

        book_ids = [
            self.gui.library_view.model().id(row.row())
            for row in rows
        ]

        backup = prefs["do_backups"]
        backup_path = prefs["backup_path"]

        tdir = tempfile.TemporaryDirectory()

        job = ThreadedJob(
            "fimfic_fix_fix_images",
            "Fixing images",
            self.run_image_fix,
            (tdir, book_ids, backup, backup_path),
            {},
            self.image_fix_finished
        )

        # Keep temp directory alive
        job.tdir = tdir

        self.gui.job_manager.run_threaded_job(job)

    def run_image_fix(tdir, book_ids, backup, backup_path, **_):
        import os
        import shutil
        from calibre_plugins.fimfic_fix.fix_images import fix_images

        db = self.gui.current_db

        results = []

        for book_id in book_ids:

            # Get EPUB location from calibre library
            epub_path = db.format_abspath(
                book_id,
                "EPUB"
            )

            if not epub_path:
                continue

            # Make a working copy
            temp_epub = os.path.join(
                tdir.name,
                f"{book_id}.epub"
            )

            shutil.copy2(epub_path, temp_epub)

            # Run your fixer
            fixed_path = fix_images(
                tdir.name,
                temp_epub,
                backup,
                backup_path
            )

            # Replace calibre's EPUB
            with open(fixed_path, "rb") as f:
                db.add_format(
                    book_id,
                    "EPUB",
                    f,
                    replace=True
                )

            results.append(book_id)

        return results

    def image_fix_finished(self, job):
        from calibre.gui2 import error_dialog, info_dialog

        if job.failed:
            error_dialog(
                self.gui,
                "Fix Images Failed",
                job.error,
                det_msg=job.traceback
            )
            return

        info_dialog(
            self.gui,
            "Fix Images",
            "Finished fixing selected books."
        )

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
        try:
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

        # Simple print TODO will remove later
        if prefs["do_backups"]:
            dialog_str = (
                f"Book: '{mi.title}' has been merged with, '{merge_path}'.\n" +
                f"\nBackup of the original saved to '{prefs['backup_path']}'")
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
