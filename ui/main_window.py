"""
Главное окно приложения
"""
import traceback
import logging
logger = logging.getLogger(__name__)

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTextEdit, QLineEdit,
    QPushButton, QLabel, QSplitter, QFormLayout,
    QComboBox, QMessageBox, QMenuBar, QMenu,
    QStatusBar, QToolBar, QFileDialog, QInputDialog,
    QSizePolicy, QApplication
)
from PyQt6.QtGui import QAction, QKeySequence, QShortcut, QFont, QIcon, QClipboard
from PyQt6.QtCore import Qt, QTimer, QSize

from core.database import DatabaseManager
from core.code_editor import CodeEditor
from ui.styles import STYLE_SHEET
from ui.themes import apply_theme, Themes


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Применяем базовые стили
        self.setStyleSheet(STYLE_SHEET)

        # Инициализация переменных
        self.current_snippet_id = None
        self.unsaved_changes = False
        self.current_theme = "Неоновая синяя"  # Тема по умолчанию
        self.theme_actions = {}  # Словарь для действий меню тем

        self.setup_ui()
        self.setup_database()
        self.setup_connections()
        self.setup_shortcuts()
        self.load_snippets()

        # Таймер для обновления времени
        self.update_time()

        # Применяем тему после создания всех виджетов
        QTimer.singleShot(100, lambda: self.change_theme(self.current_theme))

        # Таймер для периодического бэкапа (каждый час)
        self.backup_timer = QTimer()
        self.backup_timer.timeout.connect(self.create_backup)
        self.backup_timer.start(3600000)  # 1 час в миллисекундах

        # Создаём бэкап при запуске (с задержкой 5 секунд)
        QTimer.singleShot(5000, self.create_backup)

        # Проверка горячих клавиш
        QTimer.singleShot(500, self.check_shortcuts)

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Code Snippet Manager")
        self.setGeometry(100, 100, 1200, 800)

        # Создаём меню
        self.create_menu_bar()

        # Создаём тулбар
        self.create_toolbar()

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Основная область
        self.create_main_area(main_layout)

        # Статус бар
        self.create_status_bar()

    def create_menu_bar(self):
        """Создание меню"""
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("&Файл")

        new_action = QAction("&Новый сниппет", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.add_snippet)
        file_menu.addAction(new_action)

        import_action = QAction("&Импорт...", self)
        import_action.triggered.connect(self.import_snippet)
        file_menu.addAction(import_action)

        export_action = QAction("&Экспорт...", self)
        export_action.triggered.connect(self.export_snippet)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # Подменю резервного копирования
        backup_menu = file_menu.addMenu("💾 Резервное копирование")

        backup_now_action = QAction("Создать бэкап сейчас", self)
        backup_now_action.triggered.connect(self.manual_backup)
        backup_menu.addAction(backup_now_action)

        restore_action = QAction("Восстановить из бэкапа...", self)
        restore_action.triggered.connect(self.restore_from_backup)
        backup_menu.addAction(restore_action)

        open_backup_folder_action = QAction("Открыть папку с бэкапами", self)
        open_backup_folder_action.triggered.connect(self.open_backup_folder)
        backup_menu.addAction(open_backup_folder_action)

        file_menu.addSeparator()

        exit_action = QAction("&Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Правка
        edit_menu = menubar.addMenu("&Правка")

        save_action = QAction("&Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_snippet)
        edit_menu.addAction(save_action)

        delete_action = QAction("&Удалить", self)
        delete_action.setShortcut("Del")
        delete_action.triggered.connect(self.delete_snippet)
        edit_menu.addAction(delete_action)

        # Меню Вид с новыми темами
        view_menu = menubar.addMenu("&Вид")
        theme_menu = view_menu.addMenu("🎨 Тема оформления")

        # Новые названия тем
        themes = ["Неоновая синяя", "Космический фиолет", "Матрица зелень", "Тёмный карбон"]

        for theme in themes:
            action = QAction(theme, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, t=theme: self.change_theme(t))
            theme_menu.addAction(action)
            self.theme_actions[theme] = action

        # Меню Справка
        help_menu = menubar.addMenu("&Справка")

        shortcuts_action = QAction("⌨️ Горячие клавиши", self)
        # Шорткат убираем, чтобы не конфликтовать с QShortcut
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

        about_action = QAction("&О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = QToolBar("Основные инструменты")
        toolbar.setStyleSheet("QToolBar { border: none; }")
        self.addToolBar(toolbar)

        add_btn = QPushButton("➕ Новый сниппет")
        add_btn.setObjectName("successButton")
        add_btn.setMinimumHeight(36)
        add_btn.clicked.connect(self.add_snippet)
        toolbar.addWidget(add_btn)

        save_btn = QPushButton("💾 Сохранить")
        save_btn.setMinimumHeight(36)
        save_btn.clicked.connect(self.save_snippet)
        toolbar.addWidget(save_btn)

        delete_btn = QPushButton("🗑️ Удалить")
        delete_btn.setObjectName("dangerButton")
        delete_btn.setMinimumHeight(36)
        delete_btn.clicked.connect(self.delete_snippet)
        toolbar.addWidget(delete_btn)

        toolbar.addSeparator()

        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 16px;")
        toolbar.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию, тегам или коду...")
        self.search_input.setMinimumWidth(250)
        self.search_input.setMaximumWidth(350)
        toolbar.addWidget(self.search_input)

        # Растягивающийся разделитель
        separator = QWidget()
        separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(separator)

    def create_main_area(self, main_layout):
        """Создание основной области"""
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Левая панель
        left_panel = QWidget()
        left_panel.setObjectName("glassPanel")
        left_panel.setStyleSheet("""
            QWidget#glassPanel {
                background: rgba(36, 40, 55, 0.7);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 12px;
                margin: 4px;
            }
        """)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 12, 12, 12)

        header = QLabel("📚 МОИ СНИППЕТЫ")
        header.setObjectName("headerLabel")
        left_layout.addWidget(header)

        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 0, 0, 0)

        self.stats_label = QLabel("0 сниппетов")
        self.stats_label.setStyleSheet("color: #a0a8c0; font-size: 12px;")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()

        left_layout.addWidget(stats_widget)

        self.snippets_list = QListWidget()
        left_layout.addWidget(self.snippets_list)

        # Правая панель
        right_panel = QWidget()
        right_panel.setObjectName("glassPanel")
        right_panel.setStyleSheet("""
            QWidget#glassPanel {
                background: rgba(36, 40, 55, 0.7);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 12px;
                margin: 4px;
            }
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(16, 16, 16, 16)

        # Форма
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(8)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Введите название...")

        self.language_combo = QComboBox()
        languages = ["Python", "JavaScript", "Java", "C++", "C#", "PHP",
                    "HTML", "CSS", "SQL", "TypeScript", "Go", "Rust"]
        self.language_combo.addItems(languages)

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("тег1, тег2, тег3...")

        form_layout.addRow("Название:", self.title_input)
        form_layout.addRow("Язык:", self.language_combo)
        form_layout.addRow("Теги:", self.tags_input)

        right_layout.addWidget(form_widget)

        # Описание
        desc_label = QLabel("📝 ОПИСАНИЕ")
        desc_label.setStyleSheet("font-size: 11px; margin-top: 8px;")
        right_layout.addWidget(desc_label)

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.description_input.setPlaceholderText("Краткое описание сниппета...")
        right_layout.addWidget(self.description_input)

        # КОД - с кнопкой копирования
        code_header_widget = QWidget()
        code_header_layout = QHBoxLayout(code_header_widget)
        code_header_layout.setContentsMargins(0, 0, 0, 0)

        code_label = QLabel("💻 КОД")
        code_header_layout.addWidget(code_label)
        code_header_layout.addStretch()

        # Кнопка копирования (только иконка)
        self.copy_btn = QPushButton("📋")
        self.copy_btn.setObjectName("successButton")
        self.copy_btn.setMaximumWidth(40)
        self.copy_btn.setMinimumWidth(40)
        self.copy_btn.setToolTip("Копировать код (Ctrl+C)")
        self.copy_btn.clicked.connect(self.copy_code)
        code_header_layout.addWidget(self.copy_btn)

        right_layout.addWidget(code_header_widget)

        # Редактор кода
        self.code_editor = CodeEditor()
        right_layout.addWidget(self.code_editor)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])

        main_layout.addWidget(splitter)

    def create_status_bar(self):
        """Создание статус бара"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_label = QLabel("✨ Готов к работе")
        self.status_label.setStyleSheet("color: #10b981; font-weight: bold;")
        self.status_bar.addWidget(self.status_label)

        # Индикатор бэкапа
        self.backup_indicator = QLabel("💾 Бэкап: никогда")
        self.backup_indicator.setStyleSheet("color: #6b7280;")
        self.status_bar.addPermanentWidget(self.backup_indicator)

        # Подсказка о горячих клавишах
        hint_label = QLabel("⌨️ Ctrl+Shift+H - помощь")
        hint_label.setStyleSheet("color: #6b7280; font-style: italic;")
        self.status_bar.addPermanentWidget(hint_label)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #6b7280;")
        self.status_bar.addPermanentWidget(self.time_label)

    def setup_database(self):
        """Настройка базы данных"""
        try:
            self.db = DatabaseManager()
            self.status_label.setText("✅ База данных подключена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к БД: {e}")
            sys.exit(1)

    def setup_connections(self):
        """Настройка соединений"""
        self.search_input.textChanged.connect(self.search_snippets)
        self.snippets_list.itemClicked.connect(self.on_snippet_selected)
        self.language_combo.currentTextChanged.connect(
            lambda lang: self.code_editor.set_language(lang.lower())
        )
        self.title_input.textChanged.connect(self.mark_unsaved)
        self.description_input.textChanged.connect(self.mark_unsaved)
        self.code_editor.textChanged.connect(self.mark_unsaved)
        self.tags_input.textChanged.connect(self.mark_unsaved)

    def setup_shortcuts(self):
        """Настройка всех горячих клавиш"""

        # Сохраняем сниппет (Ctrl+S)
        shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_save.activated.connect(self.save_snippet)
        shortcut_save.setAutoRepeat(False)
        shortcut_save.setContext(Qt.ShortcutContext.ApplicationShortcut)

        # Фокус на поиск (Ctrl+F)
        shortcut_find = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut_find.activated.connect(lambda: self.search_input.setFocus())
        shortcut_find.setAutoRepeat(False)
        shortcut_find.setContext(Qt.ShortcutContext.ApplicationShortcut)

        # Новый сниппет (Ctrl+N)
        shortcut_new = QShortcut(QKeySequence("Ctrl+N"), self)
        shortcut_new.activated.connect(self.add_snippet)
        shortcut_new.setAutoRepeat(False)
        shortcut_new.setContext(Qt.ShortcutContext.ApplicationShortcut)

        # Выход (Ctrl+Q)
        shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)
        shortcut_quit.activated.connect(self.close)
        shortcut_quit.setAutoRepeat(False)
        shortcut_quit.setContext(Qt.ShortcutContext.ApplicationShortcut)

        # Справка (Ctrl+Shift+H)
        shortcut_help = QShortcut(QKeySequence("Ctrl+Shift+H"), self)
        shortcut_help.activated.connect(self.show_shortcuts)
        shortcut_help.setAutoRepeat(False)
        shortcut_help.setContext(Qt.ShortcutContext.ApplicationShortcut)

        # Удалить (Del) - только если есть выбранный сниппет
        shortcut_delete = QShortcut(QKeySequence("Del"), self)
        shortcut_delete.activated.connect(self.delete_snippet)
        shortcut_delete.setAutoRepeat(False)
        shortcut_delete.setContext(Qt.ShortcutContext.ApplicationShortcut)

        print("DEBUG: Все горячие клавиши настроены")

    def check_shortcuts(self):
        """Проверяет работу горячих клавиш"""
        print("DEBUG: Проверка горячих клавиш...")
        print(f"DEBUG: Есть ли code_editor? {hasattr(self, 'code_editor')}")

    def update_time(self):
        """Обновление времени"""
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        self.time_label.setText(f"🕒 {now}")
        QTimer.singleShot(60000, self.update_time)

    def update_backup_indicator(self):
        """Обновляет индикатор последнего бэкапа"""
        try:
            backup_dir = Path.home() / "CodeSnippetManager_Backups"

            if backup_dir.exists():
                backups = list(backup_dir.glob("snippets_backup_*.db"))
                if backups:
                    # Берём самый новый бэкап
                    latest = max(backups, key=lambda p: p.stat().st_mtime)
                    from datetime import datetime
                    mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                    time_str = mtime.strftime("%H:%M %d.%m.%Y")
                    self.backup_indicator.setText(f"💾 Бэкап: {time_str}")
                    return

            self.backup_indicator.setText("💾 Бэкап: никогда")
        except:
            pass

    def load_snippets(self):
        """Загрузка списка сниппетов"""
        self.snippets_list.clear()
        snippets = self.db.get_all_snippets()

        for snippet in snippets:
            title = snippet['title']
            language = snippet['language']
            tags = snippet['tags'] if snippet['tags'] else "без тегов"

            lang_icon = self.get_language_icon(language)
            display_text = f"{lang_icon} {title}  ·  🏷️ {tags}  ·  ⚡ {language}"

            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, snippet['id'])
            item.setSizeHint(QSize(0, 60))

            self.snippets_list.addItem(item)

        self.stats_label.setText(f"📊 Всего: {len(snippets)}")

    def get_language_icon(self, language):
        """Иконка для языка"""
        icons = {
            "Python": "🐍", "JavaScript": "📜", "Java": "☕",
            "C++": "⚙️", "C#": "🎯", "HTML": "🌐", "CSS": "🎨",
            "SQL": "🗄️", "TypeScript": "📘", "Go": "🔵", "Rust": "🦀"
        }
        return icons.get(language, "📄")

    def on_snippet_selected(self, item):
        """Выбор сниппета"""
        snippet_id = item.data(Qt.ItemDataRole.UserRole)
        snippet = self.db.get_snippet_by_id(snippet_id)

        if snippet:
            self.current_snippet_id = snippet_id
            self.title_input.setText(snippet['title'])

            index = self.language_combo.findText(snippet['language'])
            if index >= 0:
                self.language_combo.setCurrentIndex(index)

            self.tags_input.setText(snippet['tags'] or "")
            self.description_input.setPlainText(snippet['description'] or "")
            self.code_editor.setPlainText(snippet['code'])
            self.code_editor.set_language(snippet['language'].lower())

            self.status_label.setText(f"📂 Загружен: {snippet['title']}")
            self.unsaved_changes = False

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ СО СНИППЕТАМИ ====================

    def add_snippet(self):
        """Новый сниппет"""
        self.current_snippet_id = None
        self.title_input.clear()
        self.language_combo.setCurrentIndex(0)
        self.tags_input.clear()
        self.description_input.clear()
        self.code_editor.clear()
        self.title_input.setFocus()
        self.status_label.setText("✨ Создание нового сниппета")
        self.unsaved_changes = False

    def save_snippet(self):
        """Сохранение сниппета"""
        title = self.title_input.text().strip()
        language = self.language_combo.currentText()
        tags = self.tags_input.text().strip()
        description = self.description_input.toPlainText().strip()
        code = self.code_editor.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Предупреждение", "Введите название сниппета!")
            self.title_input.setFocus()
            return

        if not code:
            QMessageBox.warning(self, "Предупреждение", "Код не может быть пустым!")
            self.code_editor.setFocus()
            return

        try:
            if self.current_snippet_id is not None:
                self.db.update_snippet(self.current_snippet_id, title, language,
                                       description, code, tags)
                message = f"✅ Сниппет '{title}' обновлён"
            else:
                snippet_id = self.db.add_snippet(title, language, description, code, tags)
                self.current_snippet_id = snippet_id
                message = f"✅ Сниппет '{title}' создан"

            self.load_snippets()
            self.status_label.setText(message)
            self.unsaved_changes = False

            if self.current_snippet_id:
                self.select_snippet_in_list(self.current_snippet_id)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

    def delete_snippet(self):
        """Удаление сниппета"""
        if self.current_snippet_id is None:
            QMessageBox.warning(self, "Предупреждение", "Выберите сниппет для удаления!")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Удалить этот сниппет?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_snippet(self.current_snippet_id)
                self.current_snippet_id = None
                self.load_snippets()
                self.add_snippet()
                self.status_label.setText("🗑️ Сниппет удалён")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить: {e}")

    def search_snippets(self):
        """Поиск сниппетов"""
        search_text = self.search_input.text().strip()

        if not search_text:
            self.load_snippets()
            return

        self.snippets_list.clear()
        results = self.db.search_snippets(search_text)

        for snippet in results:
            title = snippet['title']
            language = snippet['language']
            tags = snippet['tags'] if snippet['tags'] else "без тегов"

            lang_icon = self.get_language_icon(language)
            display_text = f"{lang_icon} {title}  ·  🏷️ {tags}  ·  ⚡ {language}"

            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, snippet['id'])
            item.setSizeHint(QSize(0, 60))

            self.snippets_list.addItem(item)

        self.stats_label.setText(f"📊 Найдено: {len(results)}")

    def select_snippet_in_list(self, snippet_id):
        """Выделить сниппет в списке"""
        for i in range(self.snippets_list.count()):
            item = self.snippets_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == snippet_id:
                self.snippets_list.setCurrentItem(item)
                break

    def mark_unsaved(self):
        """Отметить несохранённые изменения"""
        self.unsaved_changes = True
        self.status_label.setText("✏️ Есть несохранённые изменения")

    # ==================== МЕТОДЫ ДЛЯ КОПИРОВАНИЯ ====================

    def copy_code(self):
        """Копирует код в буфер обмена"""
        try:
            if not hasattr(self, 'code_editor') or self.code_editor is None:
                QMessageBox.warning(self, "Ошибка", "Редактор кода не найден")
                return

            code = self.code_editor.toPlainText()

            if not code:
                QMessageBox.warning(self, "Предупреждение", "Нет кода для копирования!")
                return

            # Копируем в буфер обмена
            clipboard = QApplication.clipboard()
            clipboard.setText(code)

            # Визуальный feedback
            self.status_label.setText("📋 Код скопирован")

            # Меняем временно иконку кнопки
            self.copy_btn.setText("✅")

            # Возвращаем обратно через 1.5 секунды
            QTimer.singleShot(1500, self.reset_copy_button)

        except Exception as e:
            logger.error(f"Ошибка при копировании: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось скопировать: {e}")

    def reset_copy_button(self):
        """Возвращает кнопку копирования в исходное состояние"""
        try:
            if hasattr(self, 'copy_btn') and self.copy_btn:
                self.copy_btn.setText("📋")
        except:
            pass

    # ==================== МЕТОДЫ ДЛЯ ТЕМ ====================

    def change_theme(self, theme_name):
        """Смена темы оформления"""
        try:
            print(f"DEBUG: Смена темы на {theme_name}")

            # Обновляем галочки в меню
            for name, action in self.theme_actions.items():
                action.setChecked(name == theme_name)

            # Применяем тему к главному окну
            theme = apply_theme(self, theme_name)

            # Применяем тему к редактору
            self.apply_theme_to_editor(theme_name)

            # Обновляем статус
            if hasattr(self, 'status_label'):
                self.status_label.setText(f"🎨 Тема: {theme_name}")

            # Сохраняем выбранную тему
            self.current_theme = theme_name

        except Exception as e:
            logger.error(f"Ошибка при смене темы: {e}")
            traceback.print_exc()

    def apply_theme_to_editor(self, theme_name):
        """Применение темы к редактору кода"""
        if not hasattr(self, 'code_editor') or self.code_editor is None:
            print("DEBUG: Редактор ещё не создан")
            return

        try:
            theme = Themes.get_theme(theme_name)

            # Применяем стиль к редактору
            self.code_editor.setStyleSheet(f"""
                QPlainTextEdit {{
                    background-color: {theme['editor_bg']};
                    color: {theme['editor_fg']};
                    border: 1px solid {theme['panel_border']};
                    border-radius: 8px;
                    selection-background-color: {theme['editor_selection']};
                }}
            """)

            # Обновляем область номеров строк
            if hasattr(self.code_editor, 'line_number_area'):
                self.code_editor.line_number_area.update()

            print(f"DEBUG: Тема {theme_name} применена к редактору")

        except Exception as e:
            logger.error(f"Ошибка при применении темы к редактору: {e}")

    # ==================== МЕТОДЫ ДЛЯ ИМПОРТА/ЭКСПОРТА ====================

    def import_snippet(self):
        """Импорт сниппета из файла с сохранением форматирования"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Импорт сниппета", "",
            "Все файлы (*.*);;Python файлы (*.py);;JavaScript файлы (*.js);;Текстовые файлы (*.txt)"
        )

        if file_name:
            try:
                # Читаем файл в бинарном режиме
                with open(file_name, 'rb') as file:
                    content = file.read()

                # Определяем кодировку
                import chardet
                encoding = chardet.detect(content)['encoding'] or 'utf-8'

                # Декодируем
                code = content.decode(encoding, errors='ignore')

                # Нормализуем переносы строк
                code = code.replace('\r\n', '\n').replace('\r', '\n')

                # Предлагаем название
                base_name = os.path.basename(file_name)
                suggested_title = os.path.splitext(base_name)[0]

                title, ok = QInputDialog.getText(
                    self, "Импорт сниппета",
                    "Введите название для сниппета:",
                    text=suggested_title
                )

                if ok and title:
                    # Устанавливаем текст
                    self.code_editor.setPlainText(code)
                    self.title_input.setText(title)

                    # Определяем язык
                    ext = os.path.splitext(file_name)[1].lower().replace('.', '')
                    lang_map = {
                        'py': 'Python', 'js': 'JavaScript', 'html': 'HTML',
                        'css': 'CSS', 'sql': 'SQL', 'java': 'Java',
                        'cpp': 'C++', 'c': 'C++', 'cs': 'C#',
                        'php': 'PHP', 'rb': 'Ruby', 'go': 'Go',
                        'rs': 'Rust', 'ts': 'TypeScript'
                    }

                    if ext in lang_map:
                        index = self.language_combo.findText(lang_map[ext])
                        if index >= 0:
                            self.language_combo.setCurrentIndex(index)

                    lines = code.count('\n') + 1
                    self.status_label.setText(f"📥 Импортирован: {base_name} ({lines} строк)")

                    # Показываем сообщение
                    QMessageBox.information(self, "Успех",
                                            f"Файл импортирован!\n"
                                            f"Строк: {lines}\n"
                                            f"Размер: {len(code)} символов")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось импортировать:\n{str(e)}")

    def export_snippet(self):
        """Экспорт сниппета в файл с сохранением форматирования"""
        if not self.code_editor.toPlainText().strip():
            QMessageBox.warning(self, "Предупреждение", "Нет кода для экспорта!")
            return

        title = self.title_input.text().strip() or "snippet"
        # Очищаем название от недопустимых символов
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

        # Определяем расширение по языку
        lang = self.language_combo.currentText()
        ext_map = {
            'Python': 'py', 'JavaScript': 'js', 'HTML': 'html',
            'CSS': 'css', 'SQL': 'sql', 'Java': 'java',
            'C++': 'cpp', 'C#': 'cs', 'PHP': 'php',
            'Ruby': 'rb', 'Go': 'go', 'Rust': 'rs',
            'TypeScript': 'ts', 'JSON': 'json', 'XML': 'xml',
            'YAML': 'yml', 'Markdown': 'md'
        }
        ext = ext_map.get(lang, 'txt')
        default_name = f"{safe_title}.{ext}"

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Экспорт сниппета", default_name,
            f"Все файлы (*.*);;{lang} файлы (*.{ext});;Текстовые файлы (*.txt)"
        )

        if file_name:
            try:
                # Получаем код
                code = self.code_editor.toPlainText()

                # Записываем в файл с правильными переносами
                with open(file_name, 'w', encoding='utf-8', newline='\n') as file:
                    file.write(code)

                lines = code.count('\n') + 1
                self.status_label.setText(f"📤 Экспортирован: {os.path.basename(file_name)} ({lines} строк)")

                # Показываем сообщение об успехе
                QMessageBox.information(self, "Успех",
                                        f"Сниппет успешно экспортирован!\n"
                                        f"Файл: {os.path.basename(file_name)}\n"
                                        f"Строк: {lines}")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать:\n{str(e)}")

    # ==================== МЕТОДЫ ДЛЯ БЭКАПОВ ====================

    def create_backup(self):
        """Создаёт резервную копию базы данных"""
        try:
            # Папка для бэкапов
            backup_dir = Path.home() / "CodeSnippetManager_Backups"
            backup_dir.mkdir(exist_ok=True)

            # Имя файла с датой и временем
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"snippets_backup_{timestamp}.db"

            # Копируем базу данных
            import shutil
            shutil.copy2(self.db.db_path, backup_path)

            # Логируем
            logger.info(f"✅ Создан бэкап: {backup_path}")

            # Очищаем старые бэкапы (оставляем только последние 10)
            self.cleanup_old_backups(backup_dir, keep_count=10)

            # Обновляем индикатор
            self.update_backup_indicator()

            return str(backup_path)

        except Exception as e:
            logger.error(f"❌ Ошибка создания бэкапа: {e}")
            return None

    def cleanup_old_backups(self, backup_dir, keep_count=10):
        """Удаляет старые бэкапы, оставляя только последние keep_count"""
        try:
            # Получаем все файлы бэкапов
            backups = sorted(backup_dir.glob("snippets_backup_*.db"))

            # Если бэкапов больше чем нужно
            if len(backups) > keep_count:
                # Удаляем самые старые
                for old_backup in backups[:-keep_count]:
                    old_backup.unlink()
                    logger.info(f"🗑️ Удалён старый бэкап: {old_backup.name}")

        except Exception as e:
            logger.error(f"❌ Ошибка очистки бэкапов: {e}")

    def manual_backup(self):
        """Ручное создание бэкапа"""
        backup_path = self.create_backup()
        if backup_path:
            QMessageBox.information(
                self,
                "✅ Бэкап создан",
                f"Резервная копия создана:\n{backup_path}"
            )
            self.status_label.setText("💾 Резервная копия создана")
        else:
            QMessageBox.warning(
                self,
                "❌ Ошибка",
                "Не удалось создать резервную копию"
            )

    def restore_from_backup(self):
        """Восстанавливает базу данных из резервной копии"""
        backup_dir = Path.home() / "CodeSnippetManager_Backups"

        if not backup_dir.exists():
            QMessageBox.warning(self, "❌ Ошибка", "Папка с бэкапами не найдена")
            return

        # Получаем список бэкапов
        backups = list(backup_dir.glob("snippets_backup_*.db"))

        if not backups:
            QMessageBox.warning(self, "❌ Ошибка", "Нет доступных бэкапов")
            return

        # Создаём диалог выбора бэкапа
        items = [f.name for f in sorted(backups, reverse=True)]
        item, ok = QInputDialog.getItem(
            self,
            "Выберите бэкап",
            "Доступные резервные копии:",
            items,
            0,
            False
        )

        if ok and item:
            reply = QMessageBox.question(
                self,
                "⚠️ Подтверждение",
                "Восстановление из бэкапа заменит текущую базу данных. Продолжить?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    backup_path = backup_dir / item

                    # Закрываем текущее соединение с БД
                    self.db.close()

                    # Копируем бэкап
                    import shutil
                    shutil.copy2(backup_path, self.db.db_path)

                    # Переоткрываем соединение
                    self.db = DatabaseManager()

                    # Перезагружаем список сниппетов
                    self.load_snippets()

                    QMessageBox.information(
                        self,
                        "✅ Успех",
                        "База данных восстановлена из бэкапа"
                    )
                    self.status_label.setText("🔄 База данных восстановлена")

                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "❌ Ошибка",
                        f"Не удалось восстановить: {e}"
                    )

    def open_backup_folder(self):
        """Открывает папку с бэкапами в проводнике"""
        backup_dir = Path.home() / "CodeSnippetManager_Backups"

        if not backup_dir.exists():
            backup_dir.mkdir(exist_ok=True)

        # Открываем папку в проводнике
        import subprocess
        import platform

        if platform.system() == "Windows":
            subprocess.run(["explorer", str(backup_dir)])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(backup_dir)])
        else:  # Linux
            subprocess.run(["xdg-open", str(backup_dir)])

    # ==================== МЕТОДЫ ДЛЯ ГОРЯЧИХ КЛАВИШ ====================

    def show_shortcuts(self):
        """Показывает список горячих клавиш"""
        print("DEBUG: show_shortcuts вызван!")
        try:
            # Создаём сообщение с шорткатами
            shortcuts_text = """
            <h2>⌨️ Горячие клавиши</h2>
            <table border="0" cellpadding="8">
                <tr><td><b>Ctrl+N</b></td><td>Новый сниппет</td></tr>
                <tr><td><b>Ctrl+S</b></td><td>Сохранить сниппет</td></tr>
                <tr><td><b>Ctrl+F</b></td><td>Поиск (фокус на поле поиска)</td></tr>
                <tr><td><b>Ctrl+C</b></td><td>Копировать код</td></tr>
                <tr><td><b>Ctrl+D</b></td><td>Дублировать строку (в редакторе)</td></tr>
                <tr><td><b>Ctrl+/</b></td><td>Комментировать/раскомментировать</td></tr>
                <tr><td><b>Tab</b></td><td>Добавить отступ</td></tr>
                <tr><td><b>Shift+Tab</b></td><td>Убрать отступ</td></tr>
                <tr><td><b>Ctrl+Shift+H</b></td><td>Показать эту справку</td></tr>
                <tr><td><b>Ctrl+Q</b></td><td>Выход из программы</td></tr>
                <tr><td><b>Del</b></td><td>Удалить выбранный сниппет</td></tr>
            </table>
            """

            QMessageBox.information(self, "⌨️ Горячие клавиши", shortcuts_text)

        except Exception as e:
            print(f"Ошибка: {e}")
            # Ещё более простой вариант
            QMessageBox.information(self, "Горячие клавиши",
                "Ctrl+N - Новый сниппет\n"
                "Ctrl+S - Сохранить\n"
                "Ctrl+F - Поиск\n"
                "Ctrl+C - Копировать\n"
                "Ctrl+Shift+H - Эта справка\n"
                "Ctrl+Q - Выход")

    # ==================== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ====================

    def show_about(self):
        """О программе"""
        QMessageBox.about(self, "О программе",
                          "Code Snippet Manager\n\n"
                          "Версия 1.0\n\n"
                          "Менеджер для хранения фрагментов кода\n"
                          "с подсветкой синтаксиса.\n\n"
                          "Разработано на Python + PyQt6")

    def closeEvent(self, event):
        """Закрытие окна"""
        if self.unsaved_changes:
            reply = QMessageBox.question(
                self, "Несохранённые изменения",
                "У вас есть несохранённые изменения. Сохранить перед выходом?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Save:
                self.save_snippet()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
                return

        if hasattr(self, 'db'):
            self.db.close()

        event.accept()