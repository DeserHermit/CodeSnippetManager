"""
Кастомный редактор кода с подсветкой синтаксиса
"""

from PyQt6.QtWidgets import QTextEdit, QApplication
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter
from PyQt6.QtCore import Qt, QRegularExpression
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, get_all_lexers
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
import html
import logging

logger = logging.getLogger(__name__)


class SyntaxHighlighter(QSyntaxHighlighter):
    """Подсветка синтаксиса для простых языков (альтернатива Pygments)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Формат для ключевых слов Python
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(0, 0, 255))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        python_keywords = [
            'def', 'class', 'return', 'if', 'elif', 'else', 'for', 'while',
            'import', 'from', 'as', 'try', 'except', 'finally', 'with'
        ]

        for word in python_keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Формат для строк
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(163, 21, 21))
        self.highlighting_rules.append((QRegularExpression("\".*\""), string_format))
        self.highlighting_rules.append((QRegularExpression("\'.*\'"), string_format))

        # Формат для комментариев
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(0, 128, 0))
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), comment_format))

    def highlightBlock(self, text):
        """Применение правил подсветки к блоку текста"""
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(),
                               match.capturedLength(), format)


# core/code_editor.py - Обновляем класс CodeEditor

class CodeEditor(QTextEdit):
    """Расширенный текстовый редактор с подсветкой синтаксиса"""

    # Доступные стили Pygments
    AVAILABLE_STYLES = ['default', 'monokai', 'friendly', 'colorful',
                        'autumn', 'murphy', 'manni', 'pastie', 'borland']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_language = "python"
        self.current_style = "monokai"

        # Кэш для оптимизации
        self._last_text = ""
        self._last_lang = ""
        self._last_style = ""

    def setup_ui(self):
        """Настройка интерфейса редактора"""
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        self.setTabStopDistance(40)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def set_language(self, language: str):
        """Установка языка программирования"""
        self.current_language = language.lower()
        self.highlight_syntax()

    def set_style(self, style_name: str):
        """Установка цветовой схемы"""
        if style_name in self.AVAILABLE_STYLES:
            print(f"DEBUG: Установка темы {style_name}")  # Для отладки
            self.current_style = style_name
            # Принудительно сбрасываем кэш, чтобы тема применилась
            self._last_text = ""
            self._last_style = ""
            self.highlight_syntax()
        else:
            print(f"DEBUG: Тема {style_name} не найдена в доступных")

    def highlight_syntax(self):
        """Подсветка синтаксиса с использованием Pygments"""
        plain_text = self.toPlainText()

        print(f"DEBUG: Подсветка. Язык: {self.current_language}, Тема: {self.current_style}")  # Для отладки

        # Проверка на изменения (оптимизация)
        if (plain_text == self._last_text and
                self.current_language == self._last_lang and
                self.current_style == self._last_style):
            print("DEBUG: Нет изменений, пропускаем подсветку")
            return

        if not plain_text.strip():
            self._last_text = plain_text
            self._last_lang = self.current_language
            self._last_style = self.current_style
            return

        try:
            # Получаем лексер для языка
            lexer = get_lexer_by_name(self.current_language, stripall=True)
        except Exception as e:
            try:
                lexer = guess_lexer(plain_text)
                print(f"DEBUG: Язык угадан: {lexer.name}")
            except:
                from pygments.lexers import TextLexer
                lexer = TextLexer()
                print(f"DEBUG: Используется текстовый лексер: {e}")

        # Форматируем в HTML
        formatter = HtmlFormatter(
            style=self.current_style,
            noclasses=True,  # Inline стили
            linenos=False,  # Без номеров строк
            nowrap=True  # Без переноса
        )

        try:
            highlighted_html = highlight(plain_text, lexer, formatter)

            # Сохраняем текущее состояние
            current_position = self.textCursor().position()
            current_scroll = self.verticalScrollBar().value()

            # Устанавливаем HTML
            self.setHtml(highlighted_html)

            # Восстанавливаем позицию курсора и прокрутку
            cursor = self.textCursor()
            cursor.setPosition(min(current_position, len(plain_text)))
            self.setTextCursor(cursor)
            self.verticalScrollBar().setValue(current_scroll)

            # Сохраняем в кэш
            self._last_text = plain_text
            self._last_lang = self.current_language
            self._last_style = self.current_style

            print(f"DEBUG: Подсветка применена успешно")

        except Exception as e:
            print(f"DEBUG: Ошибка подсветки синтаксиса: {e}")
            self.setPlainText(plain_text)