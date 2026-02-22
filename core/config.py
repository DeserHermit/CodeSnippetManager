"""
Модуль для работы с конфигурацией и путями приложения
ИСПРАВЛЕННАЯ ВЕРСИЯ - без проблем с обратными слешами
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

def get_app_data_dir() -> Path:
    """
    Возвращает путь к папке данных приложения для текущей ОС

    Windows: C:/Users/<User>/AppData/Roaming/CodeSnippetManager/
    Linux: /home/<user>/.local/share/CodeSnippetManager/
    macOS: /Users/<user>/Library/Application Support/CodeSnippetManager/
    """
    home = Path.home()

    if sys.platform == "win32":
        # Windows - используем Path, который сам правильно обрабатывает слеши
        base_dir = home / "AppData" / "Roaming"
    elif sys.platform == "darwin":
        # macOS
        base_dir = home / "Library" / "Application Support"
    else:
        # Linux и другие
        base_dir = home / ".local" / "share"

    app_dir = base_dir / "CodeSnippetManager"
    app_dir.mkdir(parents=True, exist_ok=True)

    return app_dir

def get_database_path() -> Path:
    """Возвращает путь к файлу базы данных"""
    app_dir = get_app_data_dir()
    return app_dir / "snippets.db"

def get_config_path() -> Path:
    """Возвращает путь к файлу конфигурации"""
    app_dir = get_app_data_dir()
    return app_dir / "config.json"

class AppConfig:
    """Класс для работы с конфигурацией приложения"""

    DEFAULT_CONFIG = {
        "window": {
            "width": 1200,
            "height": 800,
            "x": 100,
            "y": 100
        },
        "editor": {
            "theme": "monokai",
            "font_size": 10,
            "font_family": "Consolas"
        },
        "recent_files": [],
        "auto_save": True,
        "backup_enabled": True,
        "backup_count": 5
    }

    def __init__(self):
        self.config_path = get_config_path()
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Если файла нет или он повреждён, создаём конфигурацию по умолчанию
        return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        """Сохранение конфигурации в файл"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Ошибка сохранения конфигурации: {e}")

    def get(self, key: str, default=None):
        """Получение значения из конфигурации"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value):
        """Установка значения в конфигурации"""
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save_config()

    def add_recent_file(self, file_path: str):
        """Добавление файла в список недавно открытых"""
        recent = self.get("recent_files", [])

        # Удаляем, если уже есть
        if file_path in recent:
            recent.remove(file_path)

        # Добавляем в начало
        recent.insert(0, file_path)

        # Ограничиваем количество
        recent = recent[:10]

        self.set("recent_files", recent)