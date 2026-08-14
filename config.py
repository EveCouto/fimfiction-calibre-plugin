from calibre.utils.config import JSONConfig
from qt.core import (QVBoxLayout, QHBoxLayout, QLabel, QFrame, QWidget,
                     QComboBox, QCheckBox, QSizePolicy, QFileDialog,
                     QPushButton, QDialog, QTextBrowser, Qt)
import os


prefs = JSONConfig('plugins/fimfic_merge_fix_evecouto_config')

prefs.defaults["do_backups"] = False
prefs.defaults["backup_path"] = ""
prefs.defaults["do_auto_fix"] = False
prefs.defaults["do_retry_fix"] = False
prefs.defaults["do_check_metadata"] = False
prefs.defaults["main_button"] = "Config Plugin"

prefs.defaults["show_merge"] = True
prefs.defaults["show_merge_full"] = True
prefs.defaults["show_fix"] = True
prefs.defaults["show_fix_retry"] = True
prefs.defaults["show_config"] = True


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

        # About Button
        self.about_button_row = QHBoxLayout()
        self.about_button = QPushButton("About Plugin")
        self.about_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.about_button.clicked.connect(self.show_about_dialog)
        self.about_button_row.addWidget(self.about_button)
        self.layout.addLayout(self.about_button_row)

        # About Button Spacer
        self.layout.addSpacing(10)
        self.about_button_spacer = QFrame()
        self.about_button_spacer.setFrameShape(QFrame.Shape.HLine)
        self.about_button_spacer.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.about_button_spacer)
        self.layout.addSpacing(10)

        # Main Button Dropdown
        self.main_button_row = QHBoxLayout()
        self.main_button_label = QLabel("Main Button Function:")
        self.main_button_row.addWidget(self.main_button_label)
        self.main_button_dropdown = QComboBox()
        self.main_button_dropdown.addItems(
            ["Merge Books", "Merge Books Full",
             "Fix Images", "Fix Images + Retry",
             "Config Plugin"])
        self.main_button_dropdown.setCurrentText(prefs["main_button"])
        self.main_button_row.addWidget(self.main_button_dropdown)
        self.layout.addLayout(self.main_button_row)

        # Main Button Spacer
        self.layout.addSpacing(10)
        self.main_button_spacer = QFrame()
        self.main_button_spacer.setFrameShape(QFrame.Shape.HLine)
        self.main_button_spacer.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.main_button_spacer)
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

        # Vertical layout attempt
        self.checkbox_row = QHBoxLayout()
        self.checkbow_col_l = QVBoxLayout()
        self.checkbow_col_r = QVBoxLayout()
        min_width1 = 120
        min_width2 = 150

        # Merge Metadata Check
        self.merge_check_row = QHBoxLayout()
        self.merge_check_label = QLabel(
            "Check Metadata \non Merge Books?")
        self.merge_check_label.setMinimumWidth(min_width1)
        self.merge_check_row.addWidget(self.merge_check_label)
        self.merge_check_checkbox = QCheckBox()
        self.merge_check_checkbox.setChecked(prefs["do_check_metadata"])
        self.merge_check_row.addWidget(self.merge_check_checkbox)
        self.checkbow_col_l.addLayout(self.merge_check_row)

        # Small Spacing
        self.checkbow_col_l.addSpacing(10)

        # Do Automatic image fix
        self.auto_fix_row = QHBoxLayout()
        self.auto_fix_check_label = QLabel(
            "Auto-run Fix Images \non Merge Books?")
        self.auto_fix_check_label.setMinimumWidth(min_width1)
        self.auto_fix_row.addWidget(self.auto_fix_check_label)
        self.auto_fix_checkbox = QCheckBox()
        self.auto_fix_checkbox.setChecked(prefs["do_auto_fix"])
        self.auto_fix_row.addWidget(self.auto_fix_checkbox)
        self.checkbow_col_l.addLayout(self.auto_fix_row)

        # Small Spacing
        self.checkbow_col_l.addSpacing(10)

        # Do retry image fix
        self.retry_fix_row = QHBoxLayout()
        self.retry_image_label = QLabel(
            "Always retry images \non Fix Images?")
        self.retry_image_label.setMinimumWidth(min_width1)
        self.retry_fix_row.addWidget(self.retry_image_label)
        self.retry_image_checkbox = QCheckBox()
        self.retry_image_checkbox.setChecked(prefs["do_retry_fix"])
        self.retry_fix_row.addWidget(self.retry_image_checkbox)
        self.checkbow_col_l.addLayout(self.retry_fix_row)

        # Show merge
        self.show_merge_row = QHBoxLayout()
        self.show_merge_label = QLabel("Show Merge Books:")
        self.show_merge_label.setMinimumWidth(min_width2)
        self.show_merge_row.addWidget(self.show_merge_label)
        self.show_merge_checkbox = QCheckBox()
        self.show_merge_checkbox.setChecked(prefs["show_merge"])
        self.show_merge_row.addWidget(self.show_merge_checkbox)
        self.checkbow_col_r.addLayout(self.show_merge_row)

        # Show merge full
        self.show_merge_full_row = QHBoxLayout()
        self.show_merge_full_label = QLabel("Show Merge Books Full:")
        self.show_merge_full_label.setMinimumWidth(min_width2)
        self.show_merge_full_row.addWidget(self.show_merge_full_label)
        self.show_merge_full_checkbox = QCheckBox()
        self.show_merge_full_checkbox.setChecked(prefs["show_merge_full"])
        self.show_merge_full_row.addWidget(self.show_merge_full_checkbox)
        self.checkbow_col_r.addLayout(self.show_merge_full_row)

        # Show fix
        self.show_fix_row = QHBoxLayout()
        self.show_fix_label = QLabel("Show Fix Images:")
        self.show_fix_label.setMinimumWidth(min_width2)
        self.show_fix_row.addWidget(self.show_fix_label)
        self.show_fix_checkbox = QCheckBox()
        self.show_fix_checkbox.setChecked(prefs["show_fix"])
        self.show_fix_row.addWidget(self.show_fix_checkbox)
        self.checkbow_col_r.addLayout(self.show_fix_row)

        # Show fix + retry
        self.show_fix_retry_row = QHBoxLayout()
        self.show_fix_retry_label = QLabel("Show Fix Images + Retry:")
        self.show_fix_retry_label.setMinimumWidth(min_width2)
        self.show_fix_retry_row.addWidget(self.show_fix_retry_label)
        self.show_fix_retry_checkbox = QCheckBox()
        self.show_fix_retry_checkbox.setChecked(prefs["show_fix_retry"])
        self.show_fix_retry_row.addWidget(self.show_fix_retry_checkbox)
        self.checkbow_col_r.addLayout(self.show_fix_retry_row)

        # Show config
        self.show_config_row = QHBoxLayout()
        self.show_config_label = QLabel("Show Config Plugin:")
        self.show_config_label.setMinimumWidth(min_width2)
        self.show_config_row.addWidget(self.show_config_label)
        self.show_config_checkbox = QCheckBox()
        self.show_config_checkbox.setChecked(prefs["show_config"])
        self.show_config_row.addWidget(self.show_config_checkbox)
        self.checkbow_col_r.addLayout(self.show_config_row)

        # Show Settings Warning
        self.checkbow_col_r.addSpacing(10)
        self.show_label = QLabel(
            "*Restart required for above*")
        font = self.show_label.font()
        font.setBold(True)
        self.show_label.setFont(font)
        self.show_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.checkbow_col_r.addWidget(self.show_label)

        # Vertical collumn merge
        self.checkbox_row.addLayout(self.checkbow_col_l)
        self.checkbox_spacer = QFrame()
        self.checkbox_spacer.setFrameShape(QFrame.Shape.VLine)
        self.checkbox_spacer.setFrameShadow(QFrame.Shadow.Sunken)
        self.checkbox_row.addWidget(self.checkbox_spacer)
        self.checkbox_row.addLayout(self.checkbow_col_r)
        self.layout.addLayout(self.checkbox_row)

        # Defaults Spacer
        self.layout.addSpacing(10)
        self.defaults_spacer = QFrame()
        self.defaults_spacer.setFrameShape(QFrame.Shape.HLine)
        self.defaults_spacer.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.defaults_spacer)
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
        self.main_button_dropdown.setCurrentText(prefs.defaults["main_button"])
        self.backup_checkbox.setChecked(prefs.defaults["do_backups"])
        self.backup_dir_button.setText(prefs.defaults["backup_path"])
        self.merge_check_checkbox.setChecked(
            prefs.defaults["do_check_metadata"])
        self.auto_fix_checkbox.setChecked(prefs.defaults["do_auto_fix"])
        self.retry_image_checkbox.setChecked(prefs.defaults["do_retry_fix"])

        self.show_merge_checkbox.setChecked(prefs.defaults["show_merge"])
        self.show_merge_full_checkbox.setChecked(
            prefs.defaults["show_merge_full"])
        self.show_fix_checkbox.setChecked(prefs.defaults["show_fix"])
        self.show_fix_retry_checkbox.setChecked(
            prefs.defaults["show_fix_retry"])
        self.show_config_checkbox.setChecked(prefs.defaults["show_config"])

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

    def show_about_dialog(self):
        # Shows an about dialog
        text = get_resources("README.html").decode('utf-8')
        dialog = QDialog(self)
        dialog.setWindowTitle("About FimFiction Ebook Plugin")
        dialog.resize(500, 500)

        layout = QVBoxLayout(dialog)

        browser = QTextBrowser()
        browser.setHtml(text)
        browser.setOpenExternalLinks(True)
        layout.addWidget(browser)

        dialog.exec()

    def save_settings(self):
        # Updates the preferences file
        prefs["main_button"] = self.main_button_dropdown.currentText()
        prefs["do_backups"] = self.backup_checkbox.isChecked()
        prefs["backup_path"] = self.backup_dir_button.text()
        prefs["do_check_metadata"] = self.merge_check_checkbox.isChecked()
        prefs["do_auto_fix"] = self.auto_fix_checkbox.isChecked()
        prefs["do_retry_fix"] = self.retry_image_checkbox.isChecked()

        prefs["show_merge"] = self.show_merge_checkbox.isChecked()
        prefs["show_merge_full"] = self.show_merge_full_checkbox.isChecked()
        prefs["show_fix"] = self.show_fix_checkbox.isChecked()
        prefs["show_fix_retry"] = self.show_fix_retry_checkbox.isChecked()
        prefs["show_config"] = self.show_config_checkbox.isChecked()
