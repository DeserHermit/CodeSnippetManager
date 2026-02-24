"""
Модуль для работы с базой данных SQLite
"""

import sqlite3
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_database_path():
    """Возвращает путь к файлу базы данных в папке AppData"""
    home = Path.home()

    if os.name == 'nt':  # Windows
        app_dir = home / "AppData" / "Roaming" / "CodeSnippetManager"
    else:  # Linux/Mac
        app_dir = home / ".local" / "share" / "CodeSnippetManager"

    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir / "snippets.db"

class DatabaseManager:
    """Управление базой данных SQLite для хранения сниппетов"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = get_database_path()

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Подключение к БД: {self.db_path}")

        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        self.migrate_database()

    def create_tables(self):
        """Создание таблиц"""
        create_snippets_table = """
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT NOT NULL,
            description TEXT,
            code TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_favorite BOOLEAN DEFAULT 0,
            category TEXT DEFAULT 'Uncategorized'
        )
        """

        create_version_table = """
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
        """

        create_trigger = """
        CREATE TRIGGER IF NOT EXISTS update_snippets_timestamp 
        AFTER UPDATE ON snippets 
        BEGIN
            UPDATE snippets SET updated_at = CURRENT_TIMESTAMP 
            WHERE id = NEW.id;
        END;
        """

        self.cursor.execute(create_snippets_table)
        self.cursor.execute(create_version_table)
        self.cursor.execute(create_trigger)
        self.connection.commit()
        logger.info("Таблицы созданы/проверены")

    def migrate_database(self):
        """Миграция базы данных"""
        self.cursor.execute("SELECT version FROM schema_version")
        result = self.cursor.fetchone()
        current_version = result[0] if result else 0

        if current_version < 1:
            try:
                self.cursor.execute("ALTER TABLE snippets ADD COLUMN is_favorite BOOLEAN DEFAULT 0")
                logger.info("Миграция версии 1 (is_favorite)")
            except sqlite3.OperationalError:
                logger.warning("Миграция 1 уже применена")

        if current_version < 2:
            try:
                self.cursor.execute("ALTER TABLE snippets ADD COLUMN category TEXT DEFAULT 'Uncategorized'")
                logger.info("Миграция версии 2 (category)")
            except sqlite3.OperationalError:
                logger.warning("Миграция 2 уже применена")

        self.cursor.execute("DELETE FROM schema_version")
        self.cursor.execute("INSERT INTO schema_version (version) VALUES (2)")
        self.connection.commit()

    def get_all_snippets(self):
        """Получение всех сниппетов"""
        query = """
        SELECT id, title, language, tags, created_at, is_favorite, category
        FROM snippets 
        ORDER BY updated_at DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_snippet_by_id(self, snippet_id: int):
        """Получение сниппета по ID"""
        query = "SELECT * FROM snippets WHERE id = ?"
        self.cursor.execute(query, (snippet_id,))
        return self.cursor.fetchone()

    def add_snippet(self, title: str, language: str, description: str, code: str, tags: str) -> int:
        """Добавление нового сниппета"""
        query = """
        INSERT INTO snippets (title, language, description, code, tags)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (title, language, description, code, tags))
        self.connection.commit()
        snippet_id = self.cursor.lastrowid
        logger.info(f"Сниппет добавлен (ID: {snippet_id})")
        return snippet_id

    def update_snippet(self, snippet_id: int, title: str, language: str,
                      description: str, code: str, tags: str):
        """Обновление сниппета"""
        query = """
        UPDATE snippets 
        SET title = ?, language = ?, description = ?, 
            code = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        self.cursor.execute(query, (title, language, description, code, tags, snippet_id))
        self.connection.commit()
        logger.info(f"Сниппет ID={snippet_id} обновлён")

    def delete_snippet(self, snippet_id: int):
        """Удаление сниппета"""
        query = "DELETE FROM snippets WHERE id = ?"
        self.cursor.execute(query, (snippet_id,))
        self.connection.commit()
        logger.info(f"Сниппет ID={snippet_id} удалён")

    def search_snippets(self, search_text: str):
        """Поиск сниппетов"""
        search_pattern = f"%{search_text}%"
        query = """
        SELECT id, title, language, tags 
        FROM snippets 
        WHERE title LIKE ? OR tags LIKE ? OR code LIKE ? OR description LIKE ?
        ORDER BY updated_at DESC
        """
        self.cursor.execute(query, (search_pattern, search_pattern,
                                   search_pattern, search_pattern))
        return self.cursor.fetchall()

    def get_favorites(self):
        """Получение избранных сниппетов"""
        query = """
        SELECT id, title, language, tags 
        FROM snippets 
        WHERE is_favorite = 1
        ORDER BY updated_at DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def toggle_favorite(self, snippet_id: int):
        """Переключение избранного"""
        query = """
        UPDATE snippets 
        SET is_favorite = NOT is_favorite 
        WHERE id = ?
        """
        self.cursor.execute(query, (snippet_id,))
        self.connection.commit()

    def close(self):
        """Закрытие соединения"""
        self.connection.close()
        logger.info("Соединение с БД закрыто")