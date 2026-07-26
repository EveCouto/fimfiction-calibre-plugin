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
        # from calibre_plugins.fimfic_fix.main import image_fix
        pass

    def open_book_merge(self):
        # from calibre_plugins.fimfic_fix.main import book_merge
        from calibre.gui2 import info_dialog, error_dialog

        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return error_dialog(self.gui, 'Error',
                                'Nothing Selected', show=True)
        elif len(rows) >= 2:
            return error_dialog(self.gui, 'Error',
                                'More than 1 Book Selected', show=True)

        row = rows[0]
        book_id = self.gui.library_view.model().id(row)
        db = self.gui.current_db.new_api
        mi = db.get_metadata(book_id)
        info_dialog(self.gui, "mergin?", f"merge {mi.title}", show=True)

    def open_config(self):
        base_plugin_object = self.interface_action_base_plugin
        do_user_config = base_plugin_object.do_user_config
        do_user_config(self.gui)

    def apply_settings(self):
        from calibre_plugins.fimfic_fix.config import prefs
        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        prefs
