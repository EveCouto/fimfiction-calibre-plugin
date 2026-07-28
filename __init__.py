from calibre.customize import InterfaceActionBase


class FimfictionEbookPlugin(InterfaceActionBase):

    name = 'Fimfiction Ebook Plugin'
    version = (1, 0, 1)
    author = 'EveCouto'
    supported_platforms = ['windows']
    description = 'Allows for fixing images and merging updated epubs'
    minimum_calibre_version = (9, 11, 0)

    actual_plugin = 'calibre_plugins.fimfic_fix.ui:InterfacePlugin'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.fimfic_fix.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        '''
        Save the settings specified by the user with config_widget.

        :param config_widget: The widget returned by :meth:`config_widget`.
        '''
        config_widget.save_settings()

        # Apply the changes
        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
