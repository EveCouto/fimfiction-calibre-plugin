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
        self.qaction.triggered.connect(self.test_print)

        # Sub menu
        self.menu = QMenu(self.gui)
        self.qaction.setMenu(self.menu)

        # Sub menu item 1
        self.create_menu_action(
            self.menu,
            unique_name="item1",
            text="item1",
            triggered=self.item1
        )

        # Sub menu item 2
        self.create_menu_action(
            self.menu,
            unique_name="config_plugin",
            text="Config Plugin",
            triggered=self.open_config
        )

    def test_print(self):
        pass

    def item1(self):
        pass

    def open_config(self):
        base_plugin_object = self.interface_action_base_plugin
        do_user_config = base_plugin_object.do_user_config
        do_user_config(self.gui)

    def apply_settings(self):
        from calibre_plugins.fimfic_fix.config import prefs
        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        prefs
