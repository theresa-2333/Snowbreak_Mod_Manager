import os
import sys
import json
import shutil
import webbrowser
from collections import defaultdict
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QLabel,
    QCheckBox, QPushButton, QFileDialog, QMessageBox, QFrame,
    QLineEdit, QSplitter, QDialog, QComboBox, QDialogButtonBox,
    QSizePolicy, QAbstractItemView, QScrollArea, QGridLayout,
    QStackedWidget
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QColor

from translations import tr, set_language, get_translator

# --- Constants ---
APP_VERSION = "0.2.2"
AUTHOR = "theresa-2333"
UPDATE_URL = "https://github.com/theresa-2333/Snowbreak_Mod_Manager" 
AVAILABLE_LANGUAGES = ["zh_CN", "en_US"]  # Available languages: Chinese, English 

# --- Configuration ---
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".snowbreak_mod_manager")
os.makedirs(CONFIG_DIR, exist_ok=True)
PROJECTS_FILE = os.path.join(CONFIG_DIR, "projects.json")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
IMAGES_DIR = os.path.join(CONFIG_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)
DISABLED_EXT = ".disabled"

# --- Light Theme (QSS) ---
LIGHT_STYLESHEET = """
/* Global */
QWidget {{
    font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    color: #1f2933;
}}

QMainWindow {{
    background-color: #eef1f5;
}}

QFrame#MainFrame, QFrame#DetailsFrame {{
    background-color: #ffffff;
    border-radius: 10px;
    padding: 8px;
    border: 1px solid #dde1e7;
}}

/* Image preview */
QLabel#DetailsImageLabel {{
    border: 1px solid #e0e4ea;
    border-radius: 8px;
    background-color: #f7f9fc;
}}

/* Inputs */
QLineEdit, QTextEdit {{
    background-color: #ffffff;
    border: 1px solid #d0d7e2;
    border-radius: 6px;
    padding: 8px 10px;
}}

QLineEdit:focus, QTextEdit:focus {{
    border-color: #2563eb;
}}

/* ComboBoxes */
QComboBox {{
    background-color: #ffffff;
    border: 1px solid #d0d7e2;
    border-radius: 6px;
    padding: 8px 10px;
    min-height: 20px;
}}

QComboBox:focus {{
    border-color: #2563eb;
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: url({check_svg_path});
    width: 12px;
    height: 12px;
}}

/* Buttons */
QPushButton {{
    background-color: #f3f4f6;
    border: 1px solid #d0d7e2;
    border-radius: 20px;
    padding: 6px 14px;
    min-height: 28px;
}}

QPushButton:hover {{
    background-color: #e5e7eb;
    border-color: #b8c1d4;
}}

QPushButton:pressed {{
    background-color: #d1d5db;
}}

QPushButton#DeleteButton {{
    background-color: #ef4444;
    color: #ffffff;
    border: none;
}}

QPushButton#DeleteButton:hover {{
    background-color: #dc2626;
}}

/* Checkboxes */
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #d0d7e2;
    background: #ffffff;
}}

QCheckBox::indicator:checked {{
    background-color: #2563eb;
    border-color: #2563eb;
    image: url({check_svg_path});
}}

/* Tree/list */
QTreeWidget {{
    border: 1px solid #e0e4ea;
    border-radius: 10px;
    background-color: #fafbff;
    outline: none;
}}

QTreeWidget::item {{
    padding: 4px 6px;
}}

QTreeWidget::item:selected {{
    background-color: #dbeafe;
    color: #111827;
}}

QHeaderView::section {{
    background-color: #f3f4f6;
    border: 1px solid #e0e4ea;
    padding: 4px 6px;
    font-weight: 600;
}}

/* Grid page (skin mod list) - light */
QFrame#GridFrame {{
    background-color: #ffffff;
    border: 1px solid #dde1e7;
    border-radius: 10px;
}}
QWidget#GridContainer {{
    background-color: #ffffff;
}}
QScrollArea#GridScrollArea {{
    background-color: #ffffff;
}}

/* ComboBox - rounded to match buttons */
QComboBox {{
    background-color: #f3f4f6;
    border: 1px solid #d0d7e2;
    border-radius: 20px;
    padding: 6px 14px;
    min-height: 28px;
}}
QComboBox:hover {{
    border-color: #b8c1d4;
}}
QComboBox::drop-down {{
    border: none;
    border-radius: 20px;
}}
QComboBox QAbstractItemView {{
    border-radius: 8px;
}}
"""

# --- Dark Theme (QSS) ---
DARK_STYLESHEET = """
/* Global */
QWidget {{
    font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    color: #e5e7eb;
}}

QMainWindow {{
    background-color: #111827;
}}

QFrame#MainFrame, QFrame#DetailsFrame {{
    background-color: #1f2937;
    border-radius: 10px;
    padding: 8px;
    border: 1px solid #374151;
}}

/* Image preview */
QLabel#DetailsImageLabel {{
    border: 1px solid #4b5563;
    border-radius: 8px;
    background-color: #111827;
}}

/* Inputs */
QLineEdit, QTextEdit {{
    background-color: #111827;
    border: 1px solid #4b5563;
    border-radius: 6px;
    padding: 8px 10px;
    color: #e5e7eb;
}}

QLineEdit:focus, QTextEdit:focus {{
    border-color: #3b82f6;
}}

/* ComboBoxes */
QComboBox {{
    background-color: #111827;
    border: 1px solid #4b5563;
    border-radius: 6px;
    padding: 8px 10px;
    min-height: 20px;
    color: #e5e7eb;
}}

QComboBox:focus {{
    border-color: #3b82f6;
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: url({check_svg_path});
    width: 12px;
    height: 12px;
}}

/* Buttons */
QPushButton {{
    background-color: #374151;
    border: 1px solid #4b5563;
    border-radius: 20px;
    padding: 6px 14px;
    min-height: 28px;
    color: #e5e7eb;
}}

QPushButton:hover {{
    background-color: #4b5563;
    border-color: #6b7280;
}}

QPushButton:pressed {{
    background-color: #1f2937;
}}

QPushButton#DeleteButton {{
    background-color: #dc2626;
    color: #ffffff;
    border: none;
}}

QPushButton#DeleteButton:hover {{
    background-color: #b91c1c;
}}

/* Checkboxes */
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #4b5563;
    background: #111827;
}}

QCheckBox::indicator:checked {{
    background-color: #3b82f6;
    border-color: #3b82f6;
    image: url({check_svg_path});
}}

/* Tree/list */
QTreeWidget {{
    border: 1px solid #4b5563;
    border-radius: 10px;
    background-color: #020617;
    outline: none;
}}

QTreeWidget::item {{
    padding: 4px 6px;
}}

QTreeWidget::item:selected {{
    background-color: #1d4ed8;
    color: #f9fafb;
}}

QHeaderView::section {{
    background-color: #111827;
    border: 1px solid #4b5563;
    color: #e5e7eb;
    padding: 4px 6px;
    font-weight: 600;
}}

QDialog {{
    background-color: #1f2937;
}}

/* ComboBox - rounded (dark) */
QComboBox {{
    background-color: #374151;
    border: 1px solid #4b5563;
    border-radius: 20px;
    padding: 6px 14px;
    min-height: 28px;
    color: #e5e7eb;
}}
QComboBox:hover {{
    border-color: #6b7280;
}}
QComboBox::drop-down {{
    border: none;
    border-radius: 20px;
}}
QComboBox QAbstractItemView {{
    border-radius: 8px;
}}

/* Grid page (skin mod list) */
QFrame#GridFrame {{
    background-color: #1f2937;
    border: 1px solid #374151;
    border-radius: 10px;
}}
QWidget#GridContainer {{
    background-color: #1f2937;
}}
QScrollArea#GridScrollArea {{
    background-color: #1f2937;
}}
"""

# --- Helper Functions and Custom Widgets ---

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ImageLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(1, 1)
        self._pixmap = QPixmap()

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self._update_scaled_pixmap()

    def resizeEvent(self, event):
        self._update_scaled_pixmap()
        super().resizeEvent(event)

    def _update_scaled_pixmap(self):
        if self._pixmap.isNull():
            super().setPixmap(QPixmap())
            return
        scaled_pixmap = self._pixmap.scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        super().setPixmap(scaled_pixmap)


class ModCard(QFrame):
    """Single mod card for grid view: image on top, name below. Click to open detail."""
    clicked = pyqtSignal(int)  # project_index

    def __init__(self, project_index, project_data, is_enabled, parent=None, dark_theme=False):
        super().__init__(parent)
        self.setObjectName("ModCard")
        self._dark = dark_theme
        self.project_index = project_index
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(140, 180)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setFixedHeight(120)
        self.img_label.setObjectName("ModCardImage")
        layout.addWidget(self.img_label)
        self.name_label = QLabel(project_data.get("name", "") or tr("no_image"))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setObjectName("ModCardName")
        layout.addWidget(self.name_label)
        self.set_enabled_style(is_enabled)
        image_path = project_data.get("image_path")
        if image_path and os.path.exists(image_path):
            self.img_label.setPixmap(
                QPixmap(image_path).scaled(128, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.img_label.setText(tr("no_image"))

    def set_enabled_style(self, enabled):
        if self._dark:
            if enabled:
                self.setStyleSheet(
                    "QFrame#ModCard { border: 2px solid #22c55e; border-radius: 10px; background-color: #14532d; }"
                    "QLabel#ModCardImage { background-color: #1f2937; border-radius: 8px; border: 1px solid #4b5563; color: #9ca3af; }"
                    "QLabel#ModCardName { color: #e5e7eb; font-weight: bold; font-size: 10pt; }"
                )
            else:
                self.setStyleSheet(
                    "QFrame#ModCard { border: 1px solid #4b5563; border-radius: 10px; background-color: #374151; }"
                    "QLabel#ModCardImage { background-color: #1f2937; border-radius: 8px; border: 1px solid #4b5563; color: #9ca3af; }"
                    "QLabel#ModCardName { color: #e5e7eb; font-weight: bold; font-size: 10pt; }"
                )
        else:
            if enabled:
                self.setStyleSheet(
                    "QFrame#ModCard { border: 2px solid #22c55e; border-radius: 10px; background-color: #dcfce7; }"
                    "QLabel#ModCardImage { background-color: #f0f0f0; border-radius: 8px; border: 1px solid #e0e0e0; }"
                    "QLabel#ModCardName { color: #1f2933; font-weight: bold; font-size: 10pt; }"
                )
            else:
                self.setStyleSheet(
                    "QFrame#ModCard { border: 1px solid #e0e4ea; border-radius: 10px; background-color: #ffffff; }"
                    "QLabel#ModCardImage { background-color: #f0f0f0; border-radius: 8px; border: 1px solid #e0e0e0; }"
                    "QLabel#ModCardName { color: #1f2933; font-weight: bold; font-size: 10pt; }"
                )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.project_index)
        super().mousePressEvent(event)


class CategoryCard(QFrame):
    """Single category card for grid view: image on top, name below. Click to navigate."""
    clicked = pyqtSignal(QTreeWidgetItem)  # category_item

    def __init__(self, category_item, parent=None, dark_theme=False):
        super().__init__(parent)
        self.setObjectName("CategoryCard")
        self._dark = dark_theme
        self.category_item = category_item
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(140, 180)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setFixedHeight(120)
        self.img_label.setObjectName("CategoryCardImage")
        layout.addWidget(self.img_label)
        self.name_label = QLabel(category_item.text(0))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setObjectName("CategoryCardName")
        layout.addWidget(self.name_label)
        self.set_style()
        # Try to find category image
        cat1 = category_item.parent().parent().text(0) if category_item.parent() and category_item.parent().parent() else ""
        cat2 = category_item.parent().text(0) if category_item.parent() else ""
        cat3 = category_item.text(0)
        image_path = os.path.join(IMAGES_DIR, f"category_{cat1}_{cat2}_{cat3}.png")
        if os.path.exists(image_path):
            self.img_label.setPixmap(
                QPixmap(image_path).scaled(128, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.img_label.setText(tr("no_image"))

    def set_style(self):
        if self._dark:
            self.setStyleSheet(
                "QFrame#CategoryCard { border: 1px solid #4b5563; border-radius: 10px; background-color: #374151; }"
                "QLabel#CategoryCardImage { background-color: #1f2937; border-radius: 8px; border: 1px solid #4b5563; color: #9ca3af; }"
                "QLabel#CategoryCardName { color: #e5e7eb; font-weight: bold; font-size: 10pt; }"
            )
        else:
            self.setStyleSheet(
                "QFrame#CategoryCard { border: 1px solid #e0e4ea; border-radius: 10px; background-color: #ffffff; }"
                "QLabel#CategoryCardImage { background-color: #f0f0f0; border-radius: 8px; border: 1px solid #e0e0e0; }"
                "QLabel#CategoryCardName { color: #1f2933; font-weight: bold; font-size: 10pt; }"
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.category_item)
        super().mousePressEvent(event)


class ModSetupDialog(QDialog):
    """Secondary dialog after adding a mod: set image, name, description."""
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.project_data = project_data
        self.setWindowTitle(tr("mod_setup_dialog_title"))
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.addWidget(QLabel(tr("mod_setup_name_hint")))
        self.name_edit = QLineEdit(project_data.get("name", ""))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel(tr("mod_setup_note_hint")))
        self.note_edit = QTextEdit(project_data.get("note", ""))
        self.note_edit.setMaximumHeight(80)
        layout.addWidget(self.note_edit)
        layout.addWidget(QLabel(tr("button_change_image")))
        img_btn = QPushButton(tr("button_browse"))
        img_btn.clicked.connect(self._pick_image)
        layout.addWidget(img_btn)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setMinimumWidth(400)

    def _pick_image(self):
        path, _ = QFileDialog.getOpenFileName(self, tr("select_image_title"), "", tr("file_filter_images"))
        if path:
            dest = os.path.join(IMAGES_DIR, os.path.basename(path))
            try:
                shutil.copyfile(path, dest)
                self.project_data["image_path"] = dest
            except OSError:
                pass

    def accept(self):
        self.project_data["name"] = self.name_edit.text().strip() or self.project_data.get("name", "")
        self.project_data["note"] = self.note_edit.toPlainText().strip()
        super().accept()


# --- Dialogs ---

class AboutDialog(QDialog):
    """'About' dialog to show application information."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("about_dialog_title"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        # Header with icon and title
        header_layout = QHBoxLayout()
        icon_label = QLabel()
        icon = QIcon(resource_path("img/cbjq.ico"))
        if not icon.isNull():
            icon_label.setPixmap(icon.pixmap(40, 40))
        header_layout.addWidget(icon_label)

        title_block = QVBoxLayout()
        title_label = QLabel(tr("message_app_info"))
        title_label.setStyleSheet("font-size: 15pt; font-weight: bold;")
        subtitle_label = QLabel(tr("message_version", version=APP_VERSION))
        subtitle_label.setStyleSheet("color: #6b7280; font-size: 9pt;")
        title_block.addWidget(title_label)
        title_block.addWidget(subtitle_label)
        header_layout.addLayout(title_block)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Author and link
        author_label = QLabel(tr("message_author", author=AUTHOR))
        author_label.setStyleSheet("font-size: 10pt;")
        layout.addWidget(author_label)

        url_label = QLabel(f'<a href="{UPDATE_URL}">{tr("button_check_update")}</a>')
        url_label.setOpenExternalLinks(True)
        url_label.setStyleSheet("font-size: 10pt;")
        layout.addWidget(url_label)

        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setMinimumWidth(420)
        self.setFixedSize(self.sizeHint())


class LanguageChangedDialog(QDialog):
    """Modern dialog shown after language change."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("language_settings"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        title_label = QLabel(tr("language_changed_title"))
        title_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
        layout.addWidget(title_label)

        body_label = QLabel(tr("language_changed_desc"))
        body_label.setWordWrap(True)
        body_label.setStyleSheet("font-size: 10pt; color: #6b7280;")
        layout.addWidget(body_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setMinimumWidth(360)
        self.setFixedSize(self.sizeHint())


class CategorySelectionDialog(QDialog):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("category_dialog_title"))
        self.categories = categories
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(tr("primary_category")))
        self.cat1_combo = QComboBox()
        self.cat1_combo.setEditable(True)
        self.cat1_combo.addItems(sorted(self.categories.keys()))
        self.cat1_combo.currentTextChanged.connect(self._update_cat2_combo)
        layout.addWidget(self.cat1_combo)
        layout.addWidget(QLabel(tr("secondary_category")))
        self.cat2_combo = QComboBox()
        self.cat2_combo.setEditable(True)
        self.cat2_combo.currentTextChanged.connect(self._update_cat3_combo)
        layout.addWidget(self.cat2_combo)
        layout.addWidget(QLabel(tr("tertiary_category")))
        self.cat3_combo = QComboBox()
        self.cat3_combo.setEditable(True)
        layout.addWidget(self.cat3_combo)
        self._update_cat2_combo(self.cat1_combo.currentText())
        layout.addWidget(QLabel(tr("select_category_image")))
        img_btn = QPushButton(tr("button_browse"))
        img_btn.clicked.connect(self._pick_category_image)
        layout.addWidget(img_btn)
        self.category_image_path = ""
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setMinimumWidth(300)

    def _update_cat2_combo(self, text):
        self.cat2_combo.clear()
        if text in self.categories:
            self.cat2_combo.addItems(sorted(self.categories[text].keys()))
        self._update_cat3_combo(self.cat2_combo.currentText())

    def _update_cat3_combo(self, text):
        self.cat3_combo.clear()
        cat1 = self.cat1_combo.currentText()
        if cat1 in self.categories and text in self.categories[cat1]:
            self.cat3_combo.addItems(sorted(self.categories[cat1][text]))

    def _pick_category_image(self):
        path, _ = QFileDialog.getOpenFileName(self, tr("select_image_title"), "", tr("file_filter_images"))
        if path:
            cat1 = self.cat1_combo.currentText().strip()
            cat2 = self.cat2_combo.currentText().strip()
            cat3 = self.cat3_combo.currentText().strip()
            if cat1 and cat2 and cat3:
                dest = os.path.join(IMAGES_DIR, f"category_{cat1}_{cat2}_{cat3}.png")
                try:
                    shutil.copyfile(path, dest)
                    self.category_image_path = dest
                except OSError:
                    pass

    def get_selected_categories(self):
        return self.cat1_combo.currentText().strip(), self.cat2_combo.currentText().strip(), self.cat3_combo.currentText().strip()

# --- Main Application Window ---

class ProjectManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.storage_path = os.path.join(os.path.expanduser("~"), "MyModProjects")
        self.projects = []
        self.current_theme = "light" # Default theme
        self.current_language = "zh_CN"  # Default language
        self._load_config()
        set_language(self.current_language)  # Set global language
        self._load_projects_data()

        self.setWindowTitle(tr("main_window_title"))
        self.resize(1280, 720)
        self.setWindowIcon(QIcon(resource_path("img/cbjq.ico")))
        
        self._setup_ui()
        self._apply_theme()  # Apply theme on startup
        self._populate_tree()
        self._update_details_panel(None)
        self.right_stacked.setCurrentWidget(self.grid_page)
        self.grid_title.setText("")
        self._clear_grid()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_frame = QFrame(objectName="MainFrame")
        main_layout.addWidget(main_frame)
        content_layout = QVBoxLayout(main_frame)
        content_layout.setSpacing(12)
        self._setup_top_bar(content_layout)
        splitter = QSplitter(Qt.Horizontal)
        content_layout.addWidget(splitter)
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Left panel header
        left_header = QLabel(tr("mods"))
        left_header.setStyleSheet("font-size: 12pt; font-weight: bold;")
        left_layout.addWidget(left_header)

        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel(tr("mod_tree_header"))
        self.project_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.project_tree.currentItemChanged.connect(self._on_item_selection_changed)
        left_layout.addWidget(self.project_tree)
        left_btn_layout = QHBoxLayout()
        enable_btn = QPushButton(tr("button_enable_selected"))
        enable_btn.clicked.connect(self.enable_selected_mods)
        disable_btn = QPushButton(tr("button_disable_selected"))
        disable_btn.clicked.connect(self.disable_selected_mods)
        add_btn = QPushButton(tr("button_add_mod"))
        add_btn.clicked.connect(self.add_project_from_file)
        delete_btn = QPushButton(tr("button_delete_mod"))
        delete_btn.setObjectName("DeleteButton")
        delete_btn.clicked.connect(self.delete_selected_projects)
        left_btn_layout.addWidget(enable_btn)
        left_btn_layout.addWidget(disable_btn)
        left_btn_layout.addStretch()
        left_btn_layout.addWidget(add_btn)
        left_btn_layout.addWidget(delete_btn)
        left_layout.addLayout(left_btn_layout)
        self._setup_details_panel()
        self._setup_grid_panel()
        self.right_stacked = QStackedWidget()
        self.right_stacked.addWidget(self.grid_page)
        self.right_stacked.addWidget(self.details_frame)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.right_stacked)
        splitter.setSizes([350, 930])

    def _setup_top_bar(self, parent_layout):
        """Creates the top bar for path, theme toggle, language selection, and about button."""
        top_layout = QHBoxLayout()
        self.multi_mod_warning_label = QLabel(" ⚠ ")
        self.multi_mod_warning_label.setStyleSheet(
            "font-size: 14pt; color: #ca8a04; padding: 2px 6px;"
        )
        self.multi_mod_warning_label.setToolTip("")
        self.multi_mod_warning_label.hide()
        top_layout.addWidget(self.multi_mod_warning_label)
        top_layout.addWidget(QLabel(tr("mod_storage_path")))

        self.path_edit = QLineEdit(self.storage_path)
        self.path_edit.setReadOnly(True)
        top_layout.addWidget(self.path_edit, 1) # Give stretch factor
        browse_btn = QPushButton(tr("button_browse"))
        browse_btn.clicked.connect(self.browse_storage_path)
        top_layout.addWidget(browse_btn)

        top_layout.addStretch() # Pushes following buttons to the right

        # Search box
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search Mods...")
        self.search_edit.textChanged.connect(self._on_search_text_changed)
        self.search_edit.setMaximumWidth(220)
        top_layout.addWidget(self.search_edit)

        # Language selection
        top_layout.addWidget(QLabel(tr("language")))
        self.language_combo = QComboBox()
        self.language_combo.addItems(AVAILABLE_LANGUAGES)
        self.language_combo.setCurrentText(self.current_language)
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        top_layout.addWidget(self.language_combo)

        theme_btn = QPushButton(tr("button_toggle_theme"))
        theme_btn.clicked.connect(self._toggle_theme)
        top_layout.addWidget(theme_btn)

        about_btn = QPushButton(tr("button_about"))
        about_btn.clicked.connect(self._show_about_dialog)
        top_layout.addWidget(about_btn)

        parent_layout.addLayout(top_layout)

    def _setup_details_panel(self):
        self.details_frame = QFrame(objectName="DetailsFrame")
        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(8, 8, 8, 8)
        details_layout.setSpacing(10)

        # Header: title + status
        header_layout = QHBoxLayout()
        self.details_title_label = QLabel(tr("mod_info"))
        self.details_title_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
        header_layout.addWidget(self.details_title_label)

        self.details_status_label = QLabel("")
        self.details_status_label.setStyleSheet(
            "padding: 2px 8px; border-radius: 10px; font-size: 9pt;"
        )
        header_layout.addStretch()
        header_layout.addWidget(self.details_status_label)
        details_layout.addLayout(header_layout)

        # Image preview
        self.details_image = ImageLabel(alignment=Qt.AlignCenter)
        self.details_image.setObjectName("DetailsImageLabel")
        self.details_image.setMinimumHeight(260)
        self.details_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        details_layout.addWidget(self.details_image, 2)

        # Name + path
        self.details_name_edit = QLineEdit()
        self.details_name_edit.setStyleSheet("font-size: 14pt; font-weight: bold;")
        details_layout.addWidget(self.details_name_edit)

        self.details_path_label = QLabel("")
        self.details_path_label.setStyleSheet("color: #6b7280; font-size: 9pt;")
        self.details_path_label.setWordWrap(True)
        details_layout.addWidget(self.details_path_label)

        # Note
        self.details_note_edit = QTextEdit()
        self.details_note_edit.setMaximumHeight(120)
        details_layout.addWidget(self.details_note_edit)

        # Controls
        controls_layout = QHBoxLayout()
        self.details_enable_check = QCheckBox(tr("enable_mod"))
        self.details_enable_check.stateChanged.connect(self._on_enable_changed)
        controls_layout.addWidget(self.details_enable_check)
        controls_layout.addStretch()
        change_image_btn = QPushButton(tr("button_change_image"))
        change_image_btn.clicked.connect(self.change_image)
        controls_layout.addWidget(change_image_btn)
        save_changes_btn = QPushButton(tr("button_save_changes"))
        save_changes_btn.clicked.connect(self.save_current_project_details)
        controls_layout.addWidget(save_changes_btn)
        details_layout.addLayout(controls_layout)
        self.details_frame.setVisible(False)

    def _setup_grid_panel(self):
        self.grid_page = QFrame(objectName="GridFrame")
        grid_layout = QVBoxLayout(self.grid_page)
        grid_layout.setContentsMargins(8, 8, 8, 8)
        self.grid_title = QLabel("")
        self.grid_title.setStyleSheet("font-size: 13pt; font-weight: bold;")
        grid_layout.addWidget(self.grid_title)
        self.grid_scroll = QScrollArea()
        self.grid_scroll.setObjectName("GridScrollArea")
        self.grid_scroll.setWidgetResizable(True)
        self.grid_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.grid_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.grid_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.grid_container = QWidget()
        self.grid_container.setObjectName("GridContainer")
        self.grid_layout_inner = QGridLayout(self.grid_container)
        self.grid_layout_inner.setSpacing(12)
        self.grid_scroll.setWidget(self.grid_container)
        grid_layout.addWidget(self.grid_scroll)

    # --- Theme Management ---
    def _apply_theme(self):
        """Applies the current theme's stylesheet to the application."""
        # 1. 根据当前主题选择正确的样式表字符串
        stylesheet = LIGHT_STYLESHEET if self.current_theme == "light" else DARK_STYLESHEET
        
        # 2. 获取图标资源的路径
        check_svg_path = resource_path("img/check.svg").replace("\\", "/")
        
        # 3. 使用 .format() 方法填充路径，并创建 final_stylesheet 变量
        #    (这很可能是您当前代码中缺失或错误的一行)
        final_stylesheet = stylesheet.format(check_svg_path=check_svg_path)
        
        # 4. 使用刚刚创建好的 final_stylesheet 变量来设置样式
        self.setStyleSheet(final_stylesheet)
        # Refresh grid so ModCards use new theme colors
        cur = self.project_tree.currentItem()
        if self.right_stacked.currentWidget() == self.grid_page and cur:
            parent = cur.parent()
            if parent is not None and parent.parent() is None:
                self._fill_grid_for_skin(cur)

    def _toggle_theme(self):
        """Switches between light and dark themes and saves the choice."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self._apply_theme()
        self._save_config()

    def _show_about_dialog(self):
        """Displays the 'About' dialog."""
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def _on_language_changed(self, language):
        """Handle language change event."""
        if language != self.current_language and language in AVAILABLE_LANGUAGES:
            self.current_language = language
            set_language(language)
            self._save_config()
            # Refresh UI text
            self._refresh_ui_text()
            dialog = LanguageChangedDialog(self)
            dialog.exec_()

    def _on_search_text_changed(self, text):
        """Filter the project tree based on search text."""
        query = text.strip().lower()
        self._filter_project_tree(query)

    def _filter_project_tree(self, query):
        """Show/hide items in the project tree according to the search query."""
        # Empty query: show everything and expand
        if not query:
            top_count = self.project_tree.topLevelItemCount()
            for i in range(top_count):
                top_item = self.project_tree.topLevelItem(i)
                self._set_item_and_children_visible(top_item, True)
            self.project_tree.expandAll()
            return

        top_count = self.project_tree.topLevelItemCount()
        for i in range(top_count):
            top_item = self.project_tree.topLevelItem(i)
            self._apply_filter_to_item(top_item, query)
        
        # Expand all visible items
        self.project_tree.expandAll()

    def _expand_matching_items(self, item, query):
        """Recursively expand items that match or have matching children."""
        child_count = item.childCount()
        for i in range(child_count):
            child = item.child(i)
            if not child.isHidden():
                # Expand all visible items that have children
                if child.childCount() > 0:
                    child.setExpanded(True)
                # Recurse
                self._expand_matching_items(child, query)

    def _apply_filter_to_item(self, item, query):
        """Return True if this item or any child matches the query."""
        # If this is a mod item, it has a project index stored in UserRole
        project_index = item.data(0, Qt.UserRole)
        matches_self = False
        if project_index is not None:
            try:
                project = self.projects[project_index]
            except (IndexError, TypeError):
                project = {}
            name = str(project.get("name", "")).lower()
            note = str(project.get("note", "")).lower()
            matches_self = (query in name) or (query in note)
        else:
            # Category items: match by their own text
            text = item.text(0).lower()
            matches_self = query in text

        # Check children
        child_count = item.childCount()
        any_child_visible = False
        for i in range(child_count):
            child = item.child(i)
            child_matches = self._apply_filter_to_item(child, query)
            any_child_visible = any_child_visible or child_matches

        visible = matches_self or any_child_visible
        item.setHidden(not visible)
        return visible

    def _set_item_and_children_visible(self, item, visible):
        item.setHidden(not visible)
        child_count = item.childCount()
        for i in range(child_count):
            self._set_item_and_children_visible(item.child(i), visible)
    
    def _refresh_ui_text(self):
        """Refresh all UI text after language change."""
        self.setWindowTitle(tr("main_window_title"))
        self.path_edit.setPlaceholderText(tr("mod_storage_path"))
        self.project_tree.setHeaderLabel(tr("mod_tree_header"))
        # Find and update buttons in left panel
        for btn in self.findChildren(QPushButton):
            if "add" in btn.text().lower() or "添加" in btn.text():
                btn.setText(tr("button_add_mod"))
            elif "delete" in btn.text().lower() or "删除" in btn.text():
                btn.setText(tr("button_delete_mod"))
            elif "browse" in btn.text().lower() or "更改" in btn.text():
                btn.setText(tr("button_browse"))
            elif "theme" in btn.text().lower() or "主题" in btn.text():
                btn.setText(tr("button_toggle_theme"))
            elif "about" in btn.text().lower() or "关于" in btn.text():
                btn.setText(tr("button_about"))
            elif "change" in btn.text().lower() or "更换" in btn.text():
                btn.setText(tr("button_change_image"))
            elif "save" in btn.text().lower() or "保存" in btn.text():
                btn.setText(tr("button_save_changes"))
            elif "enable selected" in btn.text().lower() or "启用选中" in btn.text():
                btn.setText(tr("button_enable_selected"))
            elif "disable selected" in btn.text().lower() or "禁用选中" in btn.text():
                btn.setText(tr("button_disable_selected"))
        self.details_enable_check.setText(tr("enable_mod"))
        
    # --- Data and Config Management ---
    def _load_projects_data(self):
        if not os.path.exists(PROJECTS_FILE):
            self.projects = []
            return
        try:
            with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
                self.projects = json.load(f)
        except (json.JSONDecodeError, TypeError):
            QMessageBox.critical(self, tr("error_title"), tr("error_load_projects"))
            self.projects = []

    def save_projects(self):
        with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.projects, f, ensure_ascii=False, indent=2)

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.storage_path = config.get("storage_path", self.storage_path)
                    self.current_theme = config.get("theme", "light") # Load theme
                    self.current_language = config.get("language", "zh_CN")  # Load language
            except (json.JSONDecodeError, TypeError):
                pass

    def _save_config(self):
        config = {
            "storage_path": self.storage_path,
            "theme": self.current_theme, # Save theme
            "language": self.current_language  # Save language
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def closeEvent(self, event):
        self.save_projects()
        event.accept()

    # --- Core Functionality (Remaining methods are mostly unchanged) ---
    def _populate_tree(self):
        self.project_tree.clear()
        category_items = {}
        for i, project_data in enumerate(self.projects):
            cat1_name = project_data.get("category1", tr("tree_uncategorized"))
            cat2_name = project_data.get("category2", tr("tree_default"))
            cat3_name = project_data.get("category3", tr("tree_default"))
            if cat1_name not in category_items:
                cat1_item = QTreeWidgetItem(self.project_tree, [cat1_name])
                category_items[cat1_name] = cat1_item
            cat1_item = category_items[cat1_name]
            cat2_key = f"{cat1_name}/{cat2_name}"
            if cat2_key not in category_items:
                cat2_item = QTreeWidgetItem(cat1_item, [cat2_name])
                category_items[cat2_key] = cat2_item
            cat2_item = category_items[cat2_key]
            cat3_key = f"{cat1_name}/{cat2_name}/{cat3_name}"
            if cat3_key not in category_items:
                cat3_item = QTreeWidgetItem(cat2_item, [cat3_name])
                category_items[cat3_key] = cat3_item
            cat3_item = category_items[cat3_key]
            mod_item = QTreeWidgetItem(cat3_item, [project_data["name"]])
            mod_item.setData(0, Qt.UserRole, i)
            if self._is_project_enabled(project_data):
                green = QColor("#166534") if self.current_theme == "dark" else QColor("#dcfce7")
                mod_item.setBackground(0, QBrush(green))
        self.project_tree.expandAll()
        self._update_multi_mod_warning()

    def _on_item_selection_changed(self, current_item, previous_item):
        if not current_item:
            self.right_stacked.setCurrentWidget(self.grid_page)
            self.grid_title.setText("")
            self._clear_grid()
            return
        project_index = current_item.data(0, Qt.UserRole)
        if project_index is not None:
            self.right_stacked.setCurrentWidget(self.details_frame)
            self._update_details_panel(self.projects[project_index])
            return
        parent = current_item.parent()
        if parent is not None and parent.parent() is not None and parent.parent().parent() is None:
            self.right_stacked.setCurrentWidget(self.grid_page)
            cat1 = parent.parent().text(0)
            cat2 = parent.text(0)
            cat3 = current_item.text(0)
            self.grid_title.setText(f"{cat1} — {cat2} — {cat3}")
            self._fill_grid_for_skin(current_item)
            return
        self.right_stacked.setCurrentWidget(self.grid_page)
        self.grid_title.setText("")
        self._clear_grid()

    def _is_project_enabled(self, project_data):
        path = project_data.get("path", "")
        if not path:
            return False
        enabled_path = path.replace(DISABLED_EXT, "")
        disabled_path = enabled_path + DISABLED_EXT
        return os.path.exists(enabled_path)

    def _clear_grid(self):
        while self.grid_layout_inner.count():
            item = self.grid_layout_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _fill_grid_for_skin(self, skin_item):
        self._clear_grid()
        row, col, cols = 0, 0, 4
        if skin_item.childCount() > 0 and skin_item.child(0).data(0, Qt.UserRole) is not None:
            # This is a costume level, show mods
            for i in range(skin_item.childCount()):
                mod_item = skin_item.child(i)
                idx = mod_item.data(0, Qt.UserRole)
                if idx is None:
                    continue
                try:
                    project_data = self.projects[idx]
                except (IndexError, TypeError):
                    continue
                enabled = self._is_project_enabled(project_data)
                card = ModCard(idx, project_data, enabled, self.grid_container, dark_theme=(self.current_theme == "dark"))
                card.clicked.connect(self._select_mod_and_show_detail)
                self.grid_layout_inner.addWidget(card, row, col)
                col += 1
                if col >= cols:
                    col = 0
                    row += 1
        else:
            # This is a higher level, show subcategories
            for i in range(skin_item.childCount()):
                cat_item = skin_item.child(i)
                card = CategoryCard(cat_item, self.grid_container, dark_theme=(self.current_theme == "dark"))
                card.clicked.connect(self._on_category_card_clicked)
                self.grid_layout_inner.addWidget(card, row, col)
                col += 1
                if col >= cols:
                    col = 0
                    row += 1

    def _on_category_card_clicked(self, category_item):
        self.project_tree.setCurrentItem(category_item)

    def _select_mod_and_show_detail(self, project_index):
        for i in range(self.project_tree.topLevelItemCount()):
            cat1_item = self.project_tree.topLevelItem(i)
            for j in range(cat1_item.childCount()):
                cat2_item = cat1_item.child(j)
                for k in range(cat2_item.childCount()):
                    cat3_item = cat2_item.child(k)
                    for l in range(cat3_item.childCount()):
                        mod_item = cat3_item.child(l)
                        if mod_item.data(0, Qt.UserRole) == project_index:
                            self.project_tree.setCurrentItem(mod_item)
                            return

    def _update_multi_mod_warning(self):
        enabled_per_costume = defaultdict(int)
        for p in self.projects:
            if not self._is_project_enabled(p):
                continue
            c1 = p.get("category1", "")
            c2 = p.get("category2", "")
            c3 = p.get("category3", "")
            if c1 and c2 and c3:
                enabled_per_costume[(c1, c2, c3)] += 1
        bad = [(c1, c2, c3) for (c1, c2, c3), n in enabled_per_costume.items() if n > 1]
        if bad:
            self.multi_mod_warning_label.setToolTip(
                tr("warning_multi_mod_in_costume", costume=bad[0][2])
            )
            self.multi_mod_warning_label.show()
        else:
            self.multi_mod_warning_label.hide()

    def _update_details_panel(self, project_data):
        if project_data is None:
            self.details_frame.setVisible(False)
            return
        self.details_frame.setVisible(True)
        self.details_frame.setProperty("current_project_path", project_data.get("path"))
        for widget in [self.details_name_edit, self.details_note_edit, self.details_enable_check]:
            widget.blockSignals(True)
        self.details_name_edit.setText(project_data.get("name", ""))
        self.details_note_edit.setPlainText(project_data.get("note", ""))
        image_path = project_data.get("image_path")
        if image_path and os.path.exists(image_path):
            self.details_image.setPixmap(QPixmap(image_path))
        else:
            self.details_image.setPixmap(QPixmap())
            self.details_image.setText(tr("no_image"))
        file_path = project_data.get("path", "")
        self.details_path_label.setText(file_path)
        enabled_path = file_path.replace(DISABLED_EXT, '')
        disabled_path = enabled_path + DISABLED_EXT
        is_missing = not os.path.exists(enabled_path) and not os.path.exists(disabled_path)
        self.details_enable_check.setEnabled(not is_missing)
        if is_missing:
            self.details_enable_check.setChecked(False)
            self.details_name_edit.setStyleSheet("color: red; font-size: 14pt; font-weight: bold;")
            self.details_status_label.setText(tr("mod_status_missing"))
            self.details_status_label.setStyleSheet(
                "padding: 2px 8px; border-radius: 10px; font-size: 9pt; "
                "background-color: #fee2e2; color: #b91c1c;"
            )
        else:
            self.details_name_edit.setStyleSheet("font-size: 14pt; font-weight: bold;")
            is_disabled = os.path.exists(disabled_path)
            self.details_enable_check.setChecked(not is_disabled)
            if is_disabled:
                self.details_status_label.setText(tr("mod_status_disabled"))
                self.details_status_label.setStyleSheet(
                    "padding: 2px 8px; border-radius: 10px; font-size: 9pt; "
                    "background-color: #fee2e2; color: #b91c1c;"
                )
            else:
                self.details_status_label.setText(tr("mod_status_enabled"))
                self.details_status_label.setStyleSheet(
                    "padding: 2px 8px; border-radius: 10px; font-size: 9pt; "
                    "background-color: #dcfce7; color: #15803d;"
                )
        for widget in [self.details_name_edit, self.details_note_edit, self.details_enable_check]:
            widget.blockSignals(False)

    def browse_storage_path(self):
        path = QFileDialog.getExistingDirectory(self, tr("select_folder_title"), self.storage_path)
        if path and path != self.storage_path:
            self.storage_path = path
            self.path_edit.setText(path)
            self._save_config()
            QMessageBox.information(self, tr("message_path_updated"), 
                                  tr("message_path_updated_desc", path=path))
            
    def add_project_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, tr("select_mod_file_title"), "", tr("file_filter_all"))
        if not file_path: return
        categories = defaultdict(lambda: defaultdict(set))
        for p in self.projects:
            if "category1" in p and "category2" in p and "category3" in p:
                categories[p["category1"]][p["category2"]].add(p["category3"])
        dialog = CategorySelectionDialog(categories, self)
        if not dialog.exec_(): return
        cat1, cat2, cat3 = dialog.get_selected_categories()
        if not cat1 or not cat2 or not cat3:
            QMessageBox.warning(self, tr("warning_invalid_category"), 
                              tr("warning_invalid_category_desc"))
            return
        file_name = os.path.basename(file_path)
        dest_dir = os.path.join(self.storage_path, cat1, cat2, cat3)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, file_name)
        if os.path.exists(dest_path) or os.path.exists(dest_path + DISABLED_EXT):
            QMessageBox.warning(self, tr("warning_file_exists"), 
                              tr("warning_file_exists_desc", filename=file_name))
            return
        try:
            shutil.copy(file_path, dest_path)
        except OSError as e:
            QMessageBox.critical(self, tr("error_copy_file"), 
                               tr("error_copy_file_desc", error=str(e)))
            return
        project_data = {
            "name": os.path.splitext(file_name)[0], "path": dest_path,
            "note": tr("original_file") + f" {file_name}", "image_path": "",
            "category1": cat1, "category2": cat2, "category3": cat3
        }
        self.projects.append(project_data)
        self.save_projects()
        setup_dialog = ModSetupDialog(project_data, self)
        setup_dialog.exec_()
        self.save_projects()
        self._populate_tree()
        self._update_multi_mod_warning()

    def delete_project(self):
        """Backward-compatible single delete; now delegates to batch delete."""
        self.delete_selected_projects()

    def _get_selected_project_indices(self):
        items = self.project_tree.selectedItems()
        indices = []
        for item in items:
            idx = item.data(0, Qt.UserRole)
            if idx is not None:
                indices.append(int(idx))
        # Remove duplicates and sort descending for safe deletion
        return sorted(set(indices), reverse=True)

    def enable_selected_mods(self):
        indices = self._get_selected_project_indices()
        if not indices:
            QMessageBox.warning(self, tr("warning_title"), tr("warning_select_mod"))
            return
        for idx in indices:
            try:
                project_data = self.projects[idx]
            except (IndexError, TypeError):
                continue
            file_path = project_data.get("path", "")
            self.toggle_project_enabled(file_path, True)
        self._populate_tree()
        self._update_multi_mod_warning()
        if self.project_tree.currentItem():
            current_index = self.project_tree.currentItem().data(0, Qt.UserRole)
            if current_index is not None:
                self._update_details_panel(self.projects[current_index])

    def disable_selected_mods(self):
        indices = self._get_selected_project_indices()
        if not indices:
            QMessageBox.warning(self, tr("warning_title"), tr("warning_select_mod"))
            return
        for idx in indices:
            try:
                project_data = self.projects[idx]
            except (IndexError, TypeError):
                continue
            file_path = project_data.get("path", "")
            self.toggle_project_enabled(file_path, False)
        self._populate_tree()
        self._update_multi_mod_warning()
        if self.project_tree.currentItem():
            current_index = self.project_tree.currentItem().data(0, Qt.UserRole)
            if current_index is not None:
                self._update_details_panel(self.projects[current_index])

    def delete_selected_projects(self):
        indices = self._get_selected_project_indices()
        if not indices:
            QMessageBox.warning(self, tr("warning_title"), tr("warning_select_mod"))
            return
        if len(indices) == 1:
            project_data = self.projects[indices[0]]
            question_title = tr("confirm_delete")
            question_text = tr("confirm_delete_desc", name=project_data.get("name", ""))
        else:
            question_title = tr("confirm_delete")
            question_text = tr("confirm_delete_desc_multi", count=len(indices))

        reply = QMessageBox.question(
            self,
            question_title,
            question_text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        for idx in indices:
            try:
                project_data = self.projects[idx]
            except (IndexError, TypeError):
                continue
            file_path = project_data.get("path", "")
            enabled_path = file_path.replace(DISABLED_EXT, "")
            disabled_path = enabled_path + DISABLED_EXT
            try:
                if os.path.exists(enabled_path):
                    os.remove(enabled_path)
                if os.path.exists(disabled_path):
                    os.remove(disabled_path)
            except OSError as e:
                QMessageBox.critical(
                    self, tr("error_title"), tr("error_delete_file", error=str(e))
                )
                return
            # Remove from projects list
            self.projects.pop(idx)

        self.save_projects()
        self._populate_tree()
        self._update_multi_mod_warning()
        self._update_details_panel(None)

    def save_current_project_details(self):
        current_item = self.project_tree.currentItem()
        if not current_item or current_item.data(0, Qt.UserRole) is None: return
        project_index = current_item.data(0, Qt.UserRole)
        project_data = self.projects[project_index]
        project_data["name"] = self.details_name_edit.text()
        project_data["note"] = self.details_note_edit.toPlainText()
        self.save_projects()
        current_item.setText(0, project_data["name"])
        QMessageBox.information(self, tr("message_saved"), tr("message_saved_desc"))

    def _on_enable_changed(self, state):
        file_path = self.details_frame.property("current_project_path")
        if not file_path: return
        self.toggle_project_enabled(file_path, bool(state))
        project_index = self.project_tree.currentItem().data(0, Qt.UserRole)
        self._update_details_panel(self.projects[project_index])
        
    def change_image(self):
        current_item = self.project_tree.currentItem()
        if not current_item or current_item.data(0, Qt.UserRole) is None:
            QMessageBox.warning(self, tr("warning_title"), tr("warning_select_before_image"))
            return
        file_path, _ = QFileDialog.getOpenFileName(self, tr("select_image_title"), "", tr("file_filter_images"))
        if not file_path: return
        image_name = os.path.basename(file_path)
        dest_path = os.path.join(IMAGES_DIR, image_name)
        try:
            shutil.copyfile(file_path, dest_path)
        except OSError as e:
            QMessageBox.critical(self, tr("error_copy_image"), 
                               tr("error_copy_image_desc", error=str(e)))
            return
        project_index = current_item.data(0, Qt.UserRole)
        project_data = self.projects[project_index]
        project_data["image_path"] = dest_path
        self._update_details_panel(project_data)
        
    @staticmethod
    def toggle_project_enabled(file_path, enable):
        if not file_path: return
        enabled_path = file_path.replace(DISABLED_EXT, '')
        disabled_path = enabled_path + DISABLED_EXT
        try:
            if enable and os.path.exists(disabled_path):
                os.rename(disabled_path, enabled_path)
            elif not enable and os.path.exists(enabled_path):
                os.rename(enabled_path, disabled_path)
        except OSError as e:
            QMessageBox.critical(None, tr("error_title"), 
                               tr("error_rename_file", error=str(e)))

# --- Application Entry Point ---
def main():
    app = QApplication(sys.argv)
    window = ProjectManagerWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
