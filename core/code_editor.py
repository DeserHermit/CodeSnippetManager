"""
Редактор кода с правильной подсветкой и номерами строк
ИСПРАВЛЕННАЯ ВЕРСИЯ - без рекурсии и вылетов
"""

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QTextCursor, QTextCharFormat,
    QPalette, QSyntaxHighlighter, QTextFormat
)
from PyQt6.QtCore import Qt, QRect, QSize, QTimer
import re
import logging

logger = logging.getLogger(__name__)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class PythonHighlighter(QSyntaxHighlighter):
    """Правильная подсветка синтаксиса Python"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Формат для ключевых слов
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(203, 166, 247))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'yield',
            'None', 'True', 'False', 'async', 'await'
        ]

        for word in keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((re.compile(pattern), keyword_format))

        # Формат для строк
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(166, 218, 149))
        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        self.highlighting_rules.append((re.compile(r'""".*?"""', re.DOTALL), string_format))
        self.highlighting_rules.append((re.compile(r"'''.*?'''", re.DOTALL), string_format))

        # Формат для комментариев
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(127, 132, 156))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r'#[^\n]*'), comment_format))

        # Формат для чисел
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(245, 194, 99))
        self.highlighting_rules.append((re.compile(r'\b[0-9]+\b'), number_format))
        self.highlighting_rules.append((re.compile(r'\b[0-9]*\.[0-9]+\b'), number_format))

        # Формат для функций
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(137, 180, 250))
        self.highlighting_rules.append((re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\()'), function_format))

        # Формат для декораторов
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor(245, 194, 99))
        self.highlighting_rules.append((re.compile(r'@[a-zA-Z_][a-zA-Z0-9_]*'), decorator_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)


class CodeEditor(QPlainTextEdit):
    """Редактор кода с подсветкой"""

    AVAILABLE_STYLES = ['monokai', 'default', 'friendly']

    def __init__(self, parent=None):
        super().__init__(parent)

        # Флаг для предотвращения рекурсии
        self._updating = False

        # Настройка внешнего вида
        self.setup_appearance()

        # Подсветка синтаксиса
        self.highlighter = PythonHighlighter(self.document())

        # Настройка номеров строк
        self.init_line_numbers()

        # Подключаем сигналы
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Подсветка текущей строки
        self.highlight_current_line()

    def setup_appearance(self):
        """Настройка внешнего вида"""
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        # Базовая тёмная тема
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 8px;
                selection-background-color: #45475a;
            }
        """)

    def init_line_numbers(self):
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.update_line_number_area)

        self.update_line_number_area_width()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 40 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect=None, dy=0):
        if rect is None:
            self.line_number_area.update()
        elif dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(),
                                        self.line_number_area.width(), rect.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(30, 30, 46))

        # Линия разделителя
        painter.setPen(QColor(50, 55, 70))
        painter.drawLine(self.line_number_area.width() - 1, event.rect().top(),
                        self.line_number_area.width() - 1, event.rect().bottom())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        current_block = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)

                if block_number == current_block:
                    painter.setPen(QColor(203, 166, 247))
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
                else:
                    painter.setPen(QColor(110, 115, 130))
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)

                painter.drawText(0, top, self.line_number_area.width() - 8,
                               self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        """Подсветка текущей строки"""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(45, 52, 68, 100)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def set_language(self, language):
        """Установка языка (без рекурсии)"""
        if self._updating:
            return

        self._updating = True
        try:
            # Просто сохраняем язык, подсветка уже работает через highlighter
            pass
        finally:
            self._updating = False

    def setPlainText(self, text):
        """Установка текста без рекурсии"""
        if self._updating:
            return

        self._updating = True
        try:
            super().setPlainText(text)
        finally:
            self._updating = False

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
            return
        elif event.key() == Qt.Key.Key_Backtab:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                cursor.movePosition(QTextCursor.MoveOperation.Left,
                                   QTextCursor.MoveMode.KeepAnchor, 4)
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                    return

        super().keyPressEvent(event)

        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            QTimer.singleShot(10, self.line_number_area.update)

    def text(self):
        """Получение текста"""
        return self.toPlainText()