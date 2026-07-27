from calibre.utils.config import JSONConfig
from qt.core import (QVBoxLayout, QHBoxLayout, QLabel,
                     QWidget, QCheckBox, QFileDialog, QPushButton)


prefs = JSONConfig('plugins/fimfic_fix_config')

prefs.defaults["do_backups"] = False
prefs.defaults["backup_path"] = ""


class ConfigWidget(QWidget):

    def __init__(self):
        # Layout init
        QWidget.__init__(self)
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        # Backup Checkbox
        self.row1 = QHBoxLayout()
        self.check_label = QLabel("Backup Files?")
        self.row1.addWidget(self.check_label)
        self.backup_checkbox = QCheckBox()
        self.backup_checkbox.setChecked(prefs["do_backups"])
        self.row1.addWidget(self.backup_checkbox)
        self.l.addLayout(self.row1)

        # Backup Path
        self.row2 = QHBoxLayout()
        self.dir_label = QLabel("Backup Folder:")
        self.row2.addWidget(self.dir_label)
        self.backup_dir_button = QPushButton(prefs["backup_path"])
        self.backup_dir_button.clicked.connect(self.get_backup_dir)
        self.row2.addWidget(self.backup_dir_button)
        self.l.addLayout(self.row2)

    def get_backup_dir(self):
        # Opens file dialog and sets button text
        backup_dir = QFileDialog.getExistingDirectory(
            self, "Select Backup Folder")
        if not backup_dir:
            backup_dir = prefs["backup_path"]
        self.backup_dir_button.setText(backup_dir)

    def save_settings(self):
        # Updates the preferences file
        prefs["do_backups"] = self.backup_checkbox.isChecked()
        prefs["backup_path"] = self.backup_dir_button.text()
