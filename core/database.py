"""
Модуль для работы с базой данных SQLite
ИСПРАВЛЕННАЯ ВЕРСИЯ - со всеми необходимыми методами
"""

import sqlite3
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Функция для получения пути к БД
def get_database_path():
    """Возвращает путь к файлу базы данных в папке AppData"""
    home = Path.home()

    # Для Windows
    if os.name == 'nt':
        app_dir = home / "AppData" / "Roaming" / "CodeSnippetManager"
    else:
        # Для Linux/Mac
        app_dir = home / ".local" / "share" / "CodeSnippetManager"

    # Создаём папку, если её нет
    app_dir.mkdir(parents=True, exist_ok=True)

    return app_dir / "snippets.db"

class DatabaseManager:
    """Управление базой данных SQLite для хранения сниппетов"""

    def __init__(self, db_path: Optional[str] = None):
        """
        Инициализация подключения к базе данных

        Args:
            db_path: Путь к файлу БД (если None - используется стандартный путь)
        """
        if db_path is None:
            db_path = get_database_path()

        self.db_path = Path(db_path)

        # Создаём папку для БД, если её нет
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Подключение к БД: {self.db_path}")

        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        # Включаем поддержку внешних ключей
        self.cursor.execute("PRAGMA foreign_keys = ON")

        self.create_tables()
        self.migrate_database()

    def create_tables(self):
        """Создание таблиц, если они не существуют"""
        # Таблица сниппетов
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

        # Таблица для отслеживания версии схемы
        create_version_table = """
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
        """

        # Триггер для автоматического обновления updated_at
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
        """Миграция базы данных при обновлении приложения"""
        # Получаем текущую версию
        self.cursor.execute("SELECT version FROM schema_version")
        result = self.cursor.fetchone()
        current_version = result[0] if result else 0

        logger.info(f"Текущая версия схемы БД: {current_version}")

        # Применяем миграции
        if current_version < 1:
            try:
                # Версия 1: Добавляем поле is_favorite
                self.cursor.execute("ALTER TABLE snippets ADD COLUMN is_favorite BOOLEAN DEFAULT 0")
                logger.info("Применена миграция версии 1 (is_favorite)")
            except sqlite3.OperationalError:
                logger.warning("Миграция 1 уже применена или не требуется")

        if current_version < 2:
            try:
                # Версия 2: Добавляем поле category
                self.cursor.execute("ALTER TABLE snippets ADD COLUMN category TEXT DEFAULT 'Uncategorized'")
                logger.info("Применена миграция версии 2 (category)")
            except sqlite3.OperationalError:
                logger.warning("Миграция 2 уже применена или не требуется")

        # Обновляем версию схемы
        self.cursor.execute("DELETE FROM schema_version")
        self.cursor.execute("INSERT INTO schema_version (version) VALUES (2)")
        self.connection.commit()

    # ==================== ОСНОВНЫЕ МЕТОДЫ ====================

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
        """Обновление существующего сниппета"""
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

    # ==================== ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ====================

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
        """Переключение статуса избранного"""
        query = """
        UPDATE snippets 
        SET is_favorite = NOT is_favorite 
        WHERE id = ?
        """
        self.cursor.execute(query, (snippet_id,))
        self.connection.commit()

    def get_by_category(self, category: str):
        """Получение сниппетов по категории"""
        query = """
        SELECT id, title, language, tags 
        FROM snippets 
        WHERE category = ?
        ORDER BY updated_at DESC
        """
        self.cursor.execute(query, (category,))
        return self.cursor.fetchall()

    def get_categories(self):
        """Получение всех категорий"""
        query = """
        SELECT DISTINCT category, COUNT(*) as count 
        FROM snippets 
        GROUP BY category 
        ORDER BY count DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_languages_statistics(self) -> List[Tuple[str, int]]:
        """Статистика по языкам программирования"""
        query = """
        SELECT language, COUNT(*) as count 
        FROM snippets 
        GROUP BY language 
        ORDER BY count DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_backup(self):
        """Создание резервной копии базы данных"""
        backup_path = self.db_path.with_suffix(f'.backup.{self.db_path.suffix}')

        try:
            # Создаём новое подключение для резервного копирования
            backup_conn = sqlite3.connect(str(backup_path))
            self.connection.backup(backup_conn)
            backup_conn.close()

            logger.info(f"Создана резервная копия: {backup_path}")
            return str(backup_path)
        except Exception as e:
            logger.error(f"Ошибка создания резервной копии: {e}")
            return None

    def restore_from_backup(self, backup_path: str) -> bool:
        """Восстановление из резервной копии"""
        backup_path = Path(backup_path)
        if not backup_path.exists():
            logger.error(f"Файл резервной копии не найден: {backup_path}")
            return False

        try:
            # Закрываем текущее соединение
            self.connection.close()

            # Удаляем текущую БД
            if self.db_path.exists():
                self.db_path.unlink()

            # Копируем резервную копию
            import shutil
            shutil.copy2(backup_path, self.db_path)

            # Переоткрываем соединение
            self.connection = sqlite3.connect(str(self.db_path))
            self.cursor = self.connection.cursor()

            logger.info(f"Восстановлено из резервной копии: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка восстановления из резервной копии: {e}")
            return False

    def close(self):
        """Закрытие соединения с базой данных"""
        self.connection.close()
        logger.info("Соединение с базой данных закрыто")

# Для тестирования
if __name__ == "__main__":
    # Тестируем создание базы данных
    db = DatabaseManager()
    print(f"База данных создана: {db.db_path}")

    # Добавляем тестовый сниппет
    snippet_id = db.add_snippet(
        title="Тестовая функция",
        language="Python",
        description="Простой пример",
        code="def hello():\n    print('Hello World')",
        tags="test, example"
    )
    print(f"Тестовый сниппет добавлен (ID: {snippet_id})")

    # Получаем все сниппеты
    snippets = db.get_all_snippets()
    print(f"Всего сниппетов: {len(snippets)}")

    db.close()