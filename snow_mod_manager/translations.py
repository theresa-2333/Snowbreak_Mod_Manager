# -*- coding: utf-8 -*-
"""
Multi-language support for Snowbreak Mod Manager
Supports: Chinese (zh_CN), English (en_US)
"""

TRANSLATIONS = {
    "zh_CN": {
        # Window and Dialog Titles
        "main_window_title": "Snowbreak Mod 管理器",
        "about_dialog_title": "关于 Mod 管理器",
        "category_dialog_title": "设置 Mod 分类",
        "select_image_title": "选择图片",
        "select_mod_file_title": "选择 Mod 文件",
        "select_folder_title": "选择存放路径",
        
        # Labels and Placeholders
        "mod_storage_path": "Mod 存放路径:",
        "primary_category": "一级分类 (角色名):",
        "secondary_category": "二级分类 (角色皮肤):",
        "mod_tree_header": "Mod 分类",
        "tree_uncategorized": "未分类",
        "tree_default": "默认",
        "enable_mod": "启用 Mod",
        "no_image": "无图片",
        "original_file": "原始文件:",
        
        # Buttons
        "button_browse": "更改...",
        "button_add_mod": "添加新 Mod...",
        "button_delete_mod": "删除选中 Mod",
        "button_toggle_theme": "切换主题",
        "button_about": "关于",
        "button_change_image": "更换图片",
        "button_save_changes": "保存更改",
        "button_ok": "确定",
        "button_cancel": "取消",
        "button_yes": "是",
        "button_no": "否",
        "button_check_update": "检查更新或反馈",
        
        # Messages - Informational
        "message_path_updated": "路径已更新",
        "message_path_updated_desc": "新的 Mod 存放路径已设置为:\n{path}",
        "message_saved": "已保存",
        "message_saved_desc": "更改已成功保存。",
        "message_app_info": "Snowbreak Mod 管理器",
        "message_version": "版本: {version}",
        "message_author": "作者: {author}",
        
        # Messages - Warnings
        "warning_title": "警告",
        "warning_select_mod": "请选择一个要删除的 Mod 项目。",
        "warning_select_before_image": "请先选择一个 Mod。",
        "warning_invalid_category": "分类无效",
        "warning_invalid_category_desc": "必须提供一级和二级分类。",
        "warning_file_exists": "文件已存在",
        "warning_file_exists_desc": "名为 '{filename}' 的文件已存在于目标分类中。",
        
        # Messages - Errors
        "error_title": "错误",
        "error_load_projects": "无法加载 projects.json，文件可能已损坏。",
        "error_copy_file": "文件复制失败",
        "error_copy_file_desc": "无法复制文件: {error}",
        "error_copy_image": "图片复制失败",
        "error_copy_image_desc": "无法复制图片: {error}",
        "error_delete_file": "删除文件失败: {error}",
        "error_rename_file": "重命名文件时出错: {error}",
        
        # Messages - Confirmation
        "confirm_delete": "确认删除",
        "confirm_delete_desc": "确定要永久删除 Mod '{name}' 吗？\n这将从磁盘删除文件，此操作不可撤销。",
        
        # File filters
        "file_filter_all": "所有文件 (*)",
        "file_filter_images": "图片文件 (*.png *.jpg *.jpeg)",
        
        # Status/Info
        "language": "语言",
        "theme_light": "浅色",
        "theme_dark": "深色",
        "button_back": "上一步",
        "button_next": "下一步",
        "button_finish": "完成",
        "message_theme_select": "选择您喜欢的主题风格",
        "message_setup_path": "设置 Mod 文件的存放路径",
        "message_setup_complete": "初始化完成！",
        "skins": "皮肤",
        "mods": "Mod 列表",
        "mod_info": "Mod 信息",
        "mod_name": "Mod 名称",
        "mod_note": "备注",
        "settings": "设置",
        "language_settings": "语言设置",
        "theme_settings": "主题设置",
        "path_settings": "路径设置",
        "button_apply": "应用",
    },
    
    "en_US": {
        # Window and Dialog Titles
        "main_window_title": "Snowbreak Mod Manager",
        "about_dialog_title": "About Mod Manager",
        "category_dialog_title": "Set Mod Category",
        "select_image_title": "Select Image",
        "select_mod_file_title": "Select Mod File",
        "select_folder_title": "Select Storage Path",
        
        # Labels and Placeholders
        "mod_storage_path": "Mod Storage Path:",
        "primary_category": "Primary Category (Character Name):",
        "secondary_category": "Secondary Category (Character Skin):",
        "mod_tree_header": "Mod Categories",
        "tree_uncategorized": "Uncategorized",
        "tree_default": "Default",
        "enable_mod": "Enable Mod",
        "no_image": "No Image",
        "original_file": "Original File:",
        
        # Buttons
        "button_browse": "Browse...",
        "button_add_mod": "Add New Mod...",
        "button_delete_mod": "Delete Selected Mod",
        "button_toggle_theme": "Toggle Theme",
        "button_about": "About",
        "button_change_image": "Change Image",
        "button_save_changes": "Save Changes",
        "button_ok": "OK",
        "button_cancel": "Cancel",
        "button_yes": "Yes",
        "button_no": "No",
        "button_check_update": "Check for Updates or Feedback",
        
        # Messages - Informational
        "message_path_updated": "Path Updated",
        "message_path_updated_desc": "New Mod storage path has been set to:\n{path}",
        "message_saved": "Saved",
        "message_saved_desc": "Changes have been successfully saved.",
        "message_app_info": "Snowbreak Mod Manager",
        "message_version": "Version: {version}",
        "message_author": "Author: {author}",
        
        # Messages - Warnings
        "warning_title": "Warning",
        "warning_select_mod": "Please select a Mod to delete.",
        "warning_select_before_image": "Please select a Mod first.",
        "warning_invalid_category": "Invalid Category",
        "warning_invalid_category_desc": "Both primary and secondary categories are required.",
        "warning_file_exists": "File Already Exists",
        "warning_file_exists_desc": "A file named '{filename}' already exists in the target category.",
        
        # Messages - Errors
        "error_title": "Error",
        "error_load_projects": "Unable to load projects.json, the file may be corrupted.",
        "error_copy_file": "Failed to Copy File",
        "error_copy_file_desc": "Unable to copy file: {error}",
        "error_copy_image": "Failed to Copy Image",
        "error_copy_image_desc": "Unable to copy image: {error}",
        "error_delete_file": "Failed to delete file: {error}",
        "error_rename_file": "Error renaming file: {error}",
        
        # Messages - Confirmation
        "confirm_delete": "Confirm Delete",
        "confirm_delete_desc": "Are you sure you want to permanently delete Mod '{name}'?\nThis will delete the file from disk and cannot be undone.",
        
        # File filters
        "file_filter_all": "All Files (*)",
        "file_filter_images": "Image Files (*.png *.jpg *.jpeg)",
        
        # Status/Info
        "language": "Language",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "button_back": "Previous",
        "button_next": "Next",
        "button_finish": "Finish",
        "message_theme_select": "Choose your preferred theme style",
        "message_setup_path": "Set the storage path for your Mod files",
        "message_setup_complete": "Setup complete!",
        "skins": "Skins",
        "mods": "Mod List",
        "mod_info": "Mod Info",
        "mod_name": "Mod Name",
        "mod_note": "Note",
        "settings": "Settings",
        "language_settings": "Language Settings",
        "theme_settings": "Theme Settings",
        "path_settings": "Path Settings",
        "button_apply": "Apply",
    }
}

class Translator:
    """Simple translator class for managing multi-language support."""
    
    def __init__(self, language="zh_CN"):
        """Initialize translator with specified language.
        
        Args:
            language: Language code ('zh_CN' or 'en_US'). Defaults to 'zh_CN'.
        """
        self.language = language if language in TRANSLATIONS else "zh_CN"
        self.translations = TRANSLATIONS[self.language]
    
    def set_language(self, language):
        """Switch to a different language.
        
        Args:
            language: Language code ('zh_CN' or 'en_US').
        """
        if language in TRANSLATIONS:
            self.language = language
            self.translations = TRANSLATIONS[language]
    
    def get_language(self):
        """Get current language code."""
        return self.language
    
    def get_available_languages(self):
        """Get list of available languages."""
        return list(TRANSLATIONS.keys())
    
    def tr(self, key, **kwargs):
        """Translate a key to current language.
        
        Args:
            key: Translation key.
            **kwargs: Format parameters for the translation string.
            
        Returns:
            Translated string, or the key itself if translation not found.
        """
        text = self.translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text


# Global translator instance
_translator = Translator("zh_CN")

def get_translator():
    """Get the global translator instance."""
    return _translator

def set_language(language):
    """Set the global language."""
    _translator.set_language(language)

def tr(key, **kwargs):
    """Translate using the global translator.
    
    Args:
        key: Translation key.
        **kwargs: Format parameters for the translation string.
        
    Returns:
        Translated string.
    """
    return _translator.tr(key, **kwargs)

def get_available_languages():
    """Get list of available languages."""
    return _translator.get_available_languages()

def get_language_name(lang_code):
    """Get display name for a language code.
    
    Args:
        lang_code: Language code like 'zh_CN' or 'en_US'.
        
    Returns:
        Display name for the language.
    """
    names = {
        "zh_CN": "中文 (Chinese)",
        "en_US": "English"
    }
    return names.get(lang_code, lang_code)
