from calibre.utils.config import JSONConfig
from qt.core import (QVBoxLayout, QHBoxLayout, QLabel, QFrame, QWidget,
                     QCheckBox, QSizePolicy, QFileDialog, QPushButton, Qt)
import os


prefs = JSONConfig('plugins/fimfic_fix_config')

prefs.defaults["do_backups"] = False
prefs.defaults["backup_path"] = ""
prefs.defaults["do_auto_fix"] = False
prefs.defaults["do_retry_fix"] = False


class ConfigWidget(QWidget):

    def __init__(self):
        # Layout init
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title Label
        self.title_label = QLabel("FimFiction Ebook Plugin Settings")
        font = self.title_label.font()
        font.setPointSize(font.pointSize() + 2)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Title Spacer
        self.title_spacer = QFrame()
        self.title_spacer.setFrameShape(QFrame.Shape.HLine)
        self.title_spacer.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.title_spacer)
        self.layout.addSpacing(10)

        # Backup Checkbox
        self.backup_check_row = QHBoxLayout()
        self.backup_check_label = QLabel("Backup Files?")
        self.backup_check_row.addWidget(self.backup_check_label)
        self.backup_checkbox = QCheckBox()
        self.backup_checkbox.setChecked(prefs["do_backups"])
        self.backup_check_row.addWidget(self.backup_checkbox)
        self.layout.addLayout(self.backup_check_row)
        self.backup_checkbox.toggled.connect(self.check_path)

        # Backup Path
        self.backup_path_row = QHBoxLayout()
        self.dir_label = QLabel("Backup Folder:")
        self.backup_path_row.addWidget(self.dir_label)
        self.backup_dir_button = QPushButton(prefs["backup_path"])
        self.backup_dir_button.clicked.connect(self.get_backup_dir)
        self.backup_path_row.addWidget(self.backup_dir_button)
        self.layout.addLayout(self.backup_path_row)

        # Backup Spacer
        self.layout.addSpacing(10)
        self.backup_spacer = QFrame()
        self.backup_spacer.setFrameShape(QFrame.Shape.HLine)
        self.backup_spacer.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.backup_spacer)
        self.layout.addSpacing(10)

        # Do Automatic image fix
        self.auto_fix_row = QHBoxLayout()
        self.auto_fix_check_label = QLabel(
            "Auto-run Fix Images \non Merge Book?")
        self.auto_fix_row.addWidget(self.auto_fix_check_label)
        self.auto_fix_checkbox = QCheckBox()
        self.auto_fix_checkbox.setChecked(prefs["do_auto_fix"])
        self.auto_fix_row.addWidget(self.auto_fix_checkbox)
        self.layout.addLayout(self.auto_fix_row)

        # Small Spacing
        self.layout.addSpacing(10)

        # Do retry image fix
        self.retry_fix_row = QHBoxLayout()
        self.retry_image_label = QLabel(
            "Retry failed images \non Image Fix?")
        self.retry_fix_row.addWidget(self.retry_image_label)
        self.retry_image_checkbox = QCheckBox()
        self.retry_image_checkbox.setChecked(prefs["do_retry_fix"])
        self.retry_fix_row.addWidget(self.retry_image_checkbox)
        self.layout.addLayout(self.retry_fix_row)

        # Image fix spacer
        self.layout.addSpacing(10)
        self.image_fix_spacer = QFrame()
        self.image_fix_spacer.setFrameShape(QFrame.Shape.HLine)
        self.image_fix_spacer.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.image_fix_spacer)
        self.layout.addSpacing(10)

        # Set Defaults
        self.defaults_row = QHBoxLayout()
        self.set_defaults_button = QPushButton("Reset to Default?")
        self.set_defaults_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.set_defaults_button.clicked.connect(self.set_defaults)
        self.defaults_row.addWidget(self.set_defaults_button)
        self.layout.addLayout(self.defaults_row)

        # Risizes to fit
        self.resize(self.sizeHint())

    def set_defaults(self):
        self.backup_checkbox.setChecked(prefs.defaults["do_backups"])
        self.backup_dir_button.setText(prefs.defaults["backup_path"])
        self.auto_fix_checkbox.setChecked(prefs.defaults["do_auto_fix"])
        self.retry_image_checkbox.setChecked(prefs.defaults["do_retry_fix"])
        self.resize(self.sizeHint())

    def check_path(self):
        if self.backup_checkbox.isChecked():
            if not self.backup_dir_button.text():
                self.backup_checkbox.setChecked(False)

    def get_backup_dir(self):
        # Opens file dialog and sets button text
        # Default location is downloads unless dir already selected
        default_loc = os.path.expanduser("~/Downloads")
        if self.backup_dir_button.text():
            if os.path.exists(self.backup_dir_button.text()):
                default_loc = self.backup_dir_button.text()
        backup_dir = QFileDialog.getExistingDirectory(
            self, "Select Backup Folder", default_loc)
        if not backup_dir:
            backup_dir = prefs["backup_path"]
        self.backup_dir_button.setText(backup_dir)
        self.resize(self.sizeHint())

    def save_settings(self):
        # Updates the preferences file
        prefs["do_backups"] = self.backup_checkbox.isChecked()
        prefs["backup_path"] = self.backup_dir_button.text()
        prefs["do_auto_fix"] = self.auto_fix_checkbox.isChecked()
        prefs["do_retry_fix"] = self.retry_image_checkbox.isChecked()
