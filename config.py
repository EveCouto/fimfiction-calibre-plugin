from calibre.utils.config import JSONConfig
from qt.core import QHBoxLayout, QLabel, QWidget


prefs = JSONConfig('plugins/fimfic_fix_config')


class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QHBoxLayout()
        self.setLayout(self.l)
        self.label = QLabel('Settings Page?')
        self.l.addWidget(self.label)

    def save_settings(self):
        pass
