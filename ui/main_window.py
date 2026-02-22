"""
Главное окно приложения
"""
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import sys
import os
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTextEdit, QLineEdit,
    QPushButton, QLabel, QSplitter, QFormLayout,
    QComboBox, QMessageBox, QMenuBar, QMenu,
    QStatusBar, QToolBar, QFileDialog, QInputDialog
)
from PyQt6.QtGui import (
    QAction, QIcon, QKeySequence, QShortcut, QFont
)
from PyQt6.QtCore import Qt, pyqtSignal

# Импортируем наши модули
from core.database import DatabaseManager
from core.code_editor import CodeEditor


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    # Сигналы для обновления UI
    snippets_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Инициализируем переменные
        self.current_snippet_id = None
        self.current_theme = "monokai"  # <-- ДОБАВИТЬ
        self.unsaved_changes = False

        self.setup_ui()
        self.setup_database()
        self.setup_connections()
        self.setup_shortcuts()
        self.load_snippets()

        # Устанавливаем тему по умолчанию
        self.code_editor.set_style(self.current_theme)

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Code Snippet Manager - PyCharm Edition")
        self.setGeometry(100, 100, 1200, 800)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. Создаём менюбар
        self.create_menu_bar()

        # 2. Создаём тулбар
        self.create_toolbar()

        # 3. Основная область
        self.create_main_area(main_layout)

        # 4. Статус бар
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

        # Меню Вид
        view_menu = menubar.addMenu("&Вид")

        theme_menu = view_menu.addMenu("&Тема редактора")
        self.theme_actions = {}

        from core.code_editor import CodeEditor
        for theme in CodeEditor.AVAILABLE_STYLES:
            action = QAction(theme.capitalize(), self)
            action.setCheckable(True)
            # Используем lambda с capture переменной
            action.triggered.connect(lambda checked, t=theme: self.change_theme(t))
            theme_menu.addAction(action)
            self.theme_actions[theme] = action

        # Устанавливаем Monokai по умолчанию
        if 'monokai' in self.theme_actions:
            self.theme_actions['monokai'].setChecked(True)

        # Меню Справка
        help_menu = menubar.addMenu("&Справка")

        about_action = QAction("&О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = QToolBar("Основные инструменты")
        self.addToolBar(toolbar)

        # Кнопка "Добавить"
        add_btn = QPushButton("+ Новый")
        add_btn.clicked.connect(self.add_snippet)
        toolbar.addWidget(add_btn)

        # Кнопка "Сохранить"
        save_btn = QPushButton("💾 Сохранить")
        save_btn.clicked.connect(self.save_snippet)
        toolbar.addWidget(save_btn)

        toolbar.addSeparator()

        # Поле поиска
        toolbar.addWidget(QLabel("Поиск:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_input.setMaximumWidth(200)
        toolbar.addWidget(self.search_input)

        search_btn = QPushButton("🔍")
        search_btn.clicked.connect(self.search_snippets)
        toolbar.addWidget(search_btn)

        clear_search_btn = QPushButton("❌")
        clear_search_btn.clicked.connect(self.clear_search)
        toolbar.addWidget(clear_search_btn)

    def create_main_area(self, main_layout):
        """Создание основной области"""
        # Горизонтальный сплиттер
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Левая панель: список сниппетов
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        left_layout.addWidget(QLabel("<b>Мои сниппеты</b>"))

        # Панель статистики
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        self.stats_label = QLabel("Всего: 0")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        left_layout.addWidget(stats_widget)

        # Список сниппетов
        self.snippets_list = QListWidget()
        self.snippets_list.setAlternatingRowColors(True)
        left_layout.addWidget(self.snippets_list)

        # Правая панель: редактор
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Панель информации о сниппете
        info_widget = QWidget()
        info_layout = QFormLayout(info_widget)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название сниппета...")

        self.language_combo = QComboBox()
        # Добавляем популярные языки
        languages = ["Python", "JavaScript", "Java", "C++", "C#", "PHP",
                     "HTML", "CSS", "SQL", "TypeScript", "Go", "Rust",
                     "Swift", "Kotlin", "Bash", "Plain Text"]
        self.language_combo.addItems(languages)

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("теги через запятую...")

        info_layout.addRow("Название:", self.title_input)
        info_layout.addRow("Язык:", self.language_combo)
        info_layout.addRow("Теги:", self.tags_input)

        right_layout.addWidget(info_widget)

        # Описание
        right_layout.addWidget(QLabel("<b>Описание:</b>"))
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.description_input.setPlaceholderText("Краткое описание сниппета...")
        right_layout.addWidget(self.description_input)

        # Код
        right_layout.addWidget(QLabel("<b>Код:</b>"))
        self.code_editor = CodeEditor()
        right_layout.addWidget(self.code_editor)

        # Кнопки действий
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        self.save_button = QPushButton("Сохранить сниппет")
        self.save_button.clicked.connect(self.save_snippet)

        self.delete_button = QPushButton("Удалить сниппет")
        self.delete_button.clicked.connect(self.delete_snippet)
        self.delete_button.setStyleSheet("background-color: #ff4444; color: white;")

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()

        right_layout.addWidget(button_widget)

        # Добавляем панели в сплиттер
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])

        main_layout.addWidget(splitter)

    def create_status_bar(self):
        """Создание статус бара"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово к работе")

    def setup_database(self):
        """Настройка базы данных"""
        try:
            self.db = DatabaseManager()
            self.status_bar.showMessage("База данных подключена", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка",
                                 f"Не удалось подключиться к базе данных:\n{str(e)}")
            sys.exit(1)

    def setup_connections(self):
        """Настройка соединений сигналов и слотов"""
        # Поиск
        self.search_input.textChanged.connect(self.search_snippets)

        # Выбор сниппета из списка
        self.snippets_list.itemClicked.connect(self.on_snippet_selected)

        # Изменение языка
        self.language_combo.currentTextChanged.connect(
            lambda lang: self.code_editor.set_language(lang.lower())
        )

        # Автосохранение при изменении
        self.title_input.textChanged.connect(self.mark_unsaved)
        self.description_input.textChanged.connect(self.mark_unsaved)
        self.code_editor.textChanged.connect(self.mark_unsaved)
        self.tags_input.textChanged.connect(self.mark_unsaved)

        # Сигнал обновления списка
        self.snippets_updated.connect(self.load_snippets)

    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        # Ctrl+S - Сохранить
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.save_snippet)

        # Ctrl+F - Фокус на поиск
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(
            lambda: self.search_input.setFocus()
        )

        # Ctrl+N - Новый сниппет
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.add_snippet)

        # Ctrl+Q - Выход
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)

        # Ctrl+C - Копировать (будет работать в code_editor)

    def load_snippets(self):
        """Загрузка списка сниппетов"""
        self.snippets_list.clear()
        snippets = self.db.get_all_snippets()

        for index, snippet in enumerate(snippets, start=1):
            item_text = f"{index}. {snippet['title']} [{snippet['language']}]"
            if snippet['tags']:
                item_text += f" | {snippet['tags']}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, snippet['id'])
            self.snippets_list.addItem(item)

        # Обновляем статистику
        self.stats_label.setText(f"Всего: {len(snippets)}")

    def select_snippet_in_list(self, snippet_id):
        """Выделяет сниппет в списке по его ID"""
        for i in range(self.snippets_list.count()):
            item = self.snippets_list.item(i)
            # Извлекаем ID из текста элемента (формат: "ID. Название [Язык]")
            try:
                item_id = int(item.text().split('.')[0])
                if item_id == snippet_id:
                    self.snippets_list.setCurrentItem(item)
                    break
            except (ValueError, IndexError):
                continue

    def on_snippet_selected(self, item):
        """Обработка выбора сниппета из списка"""
        # Извлекаем ID из данных элемента
        snippet_id = item.data(Qt.ItemDataRole.UserRole)

        if snippet_id:
            self.current_snippet_id = snippet_id
            snippet = self.db.get_snippet_by_id(snippet_id)

            if snippet:
                # Заполняем поля
                self.title_input.setText(snippet['title'])

                # Устанавливаем язык в комбобоксе
                index = self.language_combo.findText(snippet['language'])
                if index >= 0:
                    self.language_combo.setCurrentIndex(index)

                self.tags_input.setText(snippet['tags'] or "")
                self.description_input.setPlainText(snippet['description'] or "")

                # Устанавливаем код в редактор
                self.code_editor.setPlainText(snippet['code'])
                self.code_editor.set_language(snippet['language'].lower())

                self.status_bar.showMessage(f"Загружен: {snippet['title']}")

                # Сбрасываем флаг несохранённых изменений
                self.unsaved_changes = False

    def add_snippet(self):
        """Добавление нового сниппета"""
        # Сбрасываем текущий ID
        self.current_snippet_id = None

        # Очищаем поля
        self.title_input.clear()
        self.language_combo.setCurrentIndex(0)
        self.tags_input.clear()
        self.description_input.clear()
        self.code_editor.clear()

        # Фокус на название
        self.title_input.setFocus()

        self.status_bar.showMessage("Создание нового сниппета...")

    def save_snippet(self):
        """Сохранение сниппета"""
        logger.debug(f"Сохранение сниппета. current_snippet_id: {self.current_snippet_id}")
        # Получаем данные из полей
        title = self.title_input.text().strip()
        language = self.language_combo.currentText()
        tags = self.tags_input.text().strip()
        description = self.description_input.toPlainText().strip()
        code = self.code_editor.toPlainText().strip()

        # Проверка обязательных полей
        if not title:
            QMessageBox.warning(self, "Предупреждение",
                                "Введите название сниппета!")
            self.title_input.setFocus()
            return

        if not code:
            QMessageBox.warning(self, "Предупреждение",
                                "Код не может быть пустым!")
            self.code_editor.setFocus()
            return

        try:
            # Проверяем, редактируем ли мы существующий сниппет или создаём новый
            if self.current_snippet_id is not None:
                # Обновление существующего сниппета
                self.db.update_snippet(self.current_snippet_id, title,
                                       language, description, code, tags)
                message = f"✅ Сниппет '{title}' обновлён!"
                action = "обновлён"
            else:
                # Добавление нового сниппета
                snippet_id = self.db.add_snippet(title, language,
                                                 description, code, tags)
                self.current_snippet_id = snippet_id
                message = f"✅ Сниппет '{title}' успешно создан!"
                action = "создан"

            # Обновляем список сниппетов
            self.load_snippets()

            # Если это был новый сниппет, выделяем его в списке
            if action == "создан" and self.current_snippet_id:
                self.select_snippet_in_list(self.current_snippet_id)

            # Показываем сообщение в статус-баре
            self.status_bar.showMessage(message, 5000)  # Увеличиваем время до 5 секунд

            # Также показываем всплывающее сообщение
            QMessageBox.information(self, "Успех", message)

            # Сбрасываем флаг несохранённых изменений
            self.unsaved_changes = False

        except Exception as e:
            error_msg = f"Не удалось сохранить сниппет:\n{str(e)}"
            QMessageBox.critical(self, "Ошибка", error_msg)
            self.status_bar.showMessage("❌ Ошибка при сохранении", 3000)
            print(f"Ошибка при сохранении: {e}")

    def delete_snippet(self):
        """Удаление текущего сниппета"""
        # Проверяем, есть ли текущий сниппет
        if self.current_snippet_id is None:
            QMessageBox.warning(self, "Предупреждение",
                                "Выберите сниппет для удаления!")
            return

        # Подтверждение удаления
        reply = QMessageBox.question(
            self, 'Подтверждение удаления',
            f'Вы уверены, что хотите удалить этот сниппет (ID: {self.current_snippet_id})?\n'
            'Это действие нельзя отменить.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_snippet(self.current_snippet_id)

                # Сбрасываем текущий ID
                self.current_snippet_id = None

                # Обновляем список
                self.load_snippets()

                # Очищаем форму
                self.add_snippet()

                self.status_bar.showMessage("Сниппет удалён", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка",
                                     f"Не удалось удалить сниппет:\n{str(e)}")

    def search_snippets(self):
        """Поиск сниппетов"""
        search_text = self.search_input.text().strip()

        if not search_text:
            self.load_snippets()
            return

        # Очищаем список
        self.snippets_list.clear()

        # Выполняем поиск
        results = self.db.search_snippets(search_text)

        for index, snippet in enumerate(results, start=1):
            item_text = f"{index}. {snippet['title']} [{snippet['language']}]"
            if snippet['tags']:
                item_text += f" | {snippet['tags']}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, snippet['id'])
            self.snippets_list.addItem(item)

        # Обновляем статистику
        self.stats_label.setText(f"Найдено: {len(results)}")
        self.status_bar.showMessage(f"Найдено {len(results)} сниппетов", 2000)
    def clear_search(self):
        """Очистка поиска"""
        self.search_input.clear()
        self.load_snippets()

    def mark_unsaved(self):
        """Отметка о несохранённых изменениях"""
        self.unsaved_changes = True
        if hasattr(self, 'current_snippet_id') and self.current_snippet_id:
            self.status_bar.showMessage("Есть несохранённые изменения", 2000)

    def change_theme(self, theme_name):
        """Смена темы редактора"""
        print(f"DEBUG: Смена темы на {theme_name}")  # Для отладки

        # Устанавливаем тему в редакторе
        self.code_editor.set_style(theme_name)

        # Снимаем выделение со всех тем
        for action in self.theme_actions.values():
            action.setChecked(False)

        # Устанавливаем выделение на текущую тему
        if theme_name in self.theme_actions:
            self.theme_actions[theme_name].setChecked(True)

        # Сохраняем выбранную тему в настройках (можно в базу данных или файл)
        self.current_theme = theme_name
        self.status_bar.showMessage(f"Тема изменена на '{theme_name}'", 3000)

    def import_snippet(self):
        """Импорт сниппета из файла"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Импорт сниппета", "",
            "Все файлы (*.*);;Python файлы (*.py);;Текстовые файлы (*.txt)"
        )

        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    code = file.read()

                # Предлагаем пользователю ввести название
                title, ok = QInputDialog.getText(
                    self, "Импорт сниппета",
                    "Введите название для сниппета:",
                    text=os.path.basename(file_name)
                )

                if ok and title:
                    self.code_editor.setPlainText(code)
                    self.title_input.setText(title)

                    # Пытаемся определить язык по расширению
                    ext = os.path.splitext(file_name)[1].lower()
                    lang_map = {'.py': 'Python', '.js': 'JavaScript',
                                '.html': 'HTML', '.css': 'CSS',
                                '.sql': 'SQL', '.java': 'Java'}

                    language = lang_map.get(ext, 'Plain Text')
                    index = self.language_combo.findText(language)
                    if index >= 0:
                        self.language_combo.setCurrentIndex(index)

                    self.status_bar.showMessage(f"Файл '{file_name}' загружен", 3000)

            except Exception as e:
                QMessageBox.critical(self, "Ошибка",
                                     f"Не удалось загрузить файл:\n{str(e)}")

    def export_snippet(self):
        """Экспорт сниппета в файл"""
        if not self.code_editor.toPlainText().strip():
            QMessageBox.warning(self, "Предупреждение", "Нет кода для экспорта!")
            return

        # Предлагаем имя файла на основе названия
        title = self.title_input.text().strip() or "snippet"
        default_name = f"{title}.txt"

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Экспорт сниппета", default_name,
            "Текстовые файлы (*.txt);;Все файлы (*.*)"
        )

        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(self.code_editor.toPlainText())

                self.status_bar.showMessage(f"Сниппет экспортирован в '{file_name}'", 3000)

            except Exception as e:
                QMessageBox.critical(self, "Ошибка",
                                     f"Не удалось экспортировать файл:\n{str(e)}")

    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
        <h2>Code Snippet Manager</h2>
        <p>Версия 1.0 (PyCharm Edition)</p>
        <p>Программа для хранения и управления фрагментами кода.</p>
        <p>Разработано для учебного проекта 10 класса.</p>
        <p><b>Функции:</b></p>
        <ul>
            <li>Хранение фрагментов кода с метаданными</li>
            <li>Подсветка синтаксиса для 20+ языков</li>
            <li>Поиск по названию, тегам и коду</li>
            <li>Импорт/экспорт файлов</li>
            <li>Смена тем оформления</li>
        </ul>
        <p>Используемые технологии: Python, PyQt6, SQLite, Pygments</p>
        """

        QMessageBox.about(self, "О программе", about_text)

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        # Используем getattr с значением по умолчанию, если атрибута нет
        has_unsaved = getattr(self, 'unsaved_changes', False)

        if has_unsaved:
            reply = QMessageBox.question(
                self, 'Несохранённые изменения',
                'У вас есть несохранённые изменения. Сохранить перед выходом?',
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )

            if reply == QMessageBox.StandardButton.Save:
                self.save_snippet()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            # Закрываем базу данных
            if hasattr(self, 'db'):
                self.db.close()
            event.accept()


# Для тестирования окна отдельно
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())