from calibre.gui2.actions import InterfaceAction


class FimfictionInterfaceAction(InterfaceAction):
    name = "fimfiction-tool"


def genesis(self):
    icon = get_icons('images/icon.png')
    self.quaction.setIcon(icon)

    ...
