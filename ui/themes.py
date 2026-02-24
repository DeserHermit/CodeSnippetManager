"""
Ультрасовременный дизайн 2025 с эффектом стекла и неоновыми градиентами
"""

class Themes:
    """Класс с футуристическими темами 2025"""

    @staticmethod
    def get_theme(name):
        themes = {
            "Неоновая синяя": Themes.neon_blue(),
            "Космический фиолет": Themes.space_purple(),
            "Матрица зелень": Themes.matrix_green(),
            "Тёмный карбон": Themes.dark_carbon(),
        }
        return themes.get(name, themes["Неоновая синяя"])

    @staticmethod
    def neon_blue():
        """Неоновая синяя тема"""
        return {
            "name": "Неоновая синяя",
            # Фон с космическим градиентом
            "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                      "stop:0 #0a0f1e, stop:0.5 #0f1a2f, stop:1 #0a1428)",

            # Панели с эффектом матового стекла
            "panel_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                       "stop:0 rgba(30, 40, 70, 0.4), stop:1 rgba(20, 30, 60, 0.5))",
            "panel_border": "rgba(0, 200, 255, 0.3)",
            "panel_glow": "rgba(0, 200, 255, 0.2)",

            # Текст
            "text": "#ffffff",
            "text_secondary": "rgba(255, 255, 255, 0.7)",
            "text_muted": "rgba(255, 255, 255, 0.5)",

            # Неоновые цвета
            "accent": "#00ccff",
            "accent_light": "#80ffff",
            "accent_dark": "#0099cc",
            "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, "
                              "stop:0 #00ccff, stop:0.5 #4d79ff, stop:1 #aa80ff)",

            # Цвета для кнопок
            "success": "#00ffaa",
            "error": "#ff4466",
            "warning": "#ffaa00",

            # Редактор кода
            "editor_bg": "#0a1428",
            "editor_fg": "#ffffff",
            "editor_selection": "#00ccff",
            "line_numbers": "#1a2a40",
            "current_line": "rgba(0, 200, 255, 0.1)",

            # Эффекты
            "glow": "rgba(0, 200, 255, 0.6)",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "glass": "rgba(255, 255, 255, 0.1)",
        }

    @staticmethod
    def space_purple():
        """Космический фиолет"""
        return {
            "name": "Космический фиолет",
            "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                      "stop:0 #1a0b2e, stop:0.5 #2d1b4d, stop:1 #1f0f3a)",

            "panel_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                       "stop:0 rgba(60, 30, 90, 0.4), stop:1 rgba(40, 20, 70, 0.5))",
            "panel_border": "rgba(170, 100, 255, 0.3)",
            "panel_glow": "rgba(170, 100, 255, 0.2)",

            "text": "#ffffff",
            "text_secondary": "rgba(255, 255, 255, 0.7)",
            "text_muted": "rgba(255, 255, 255, 0.5)",

            "accent": "#aa66ff",
            "accent_light": "#cc99ff",
            "accent_dark": "#8844cc",
            "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, "
                              "stop:0 #aa66ff, stop:0.5 #cc66ff, stop:1 #ff66cc)",

            "success": "#00ffaa",
            "error": "#ff4466",
            "warning": "#ffaa00",

            "editor_bg": "#1f0f3a",
            "editor_fg": "#ffffff",
            "editor_selection": "#aa66ff",
            "line_numbers": "#2d1b4d",
            "current_line": "rgba(170, 100, 255, 0.1)",

            "glow": "rgba(170, 100, 255, 0.6)",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "glass": "rgba(255, 255, 255, 0.1)",
        }

    @staticmethod
    def matrix_green():
        """Матрица зелень"""
        return {
            "name": "Матрица зелень",
            "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                      "stop:0 #0a1f0a, stop:0.5 #0f2b0f, stop:1 #0a200a)",

            "panel_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                       "stop:0 rgba(0, 50, 0, 0.4), stop:1 rgba(0, 40, 0, 0.5))",
            "panel_border": "rgba(0, 255, 100, 0.3)",
            "panel_glow": "rgba(0, 255, 100, 0.2)",

            "text": "#ffffff",
            "text_secondary": "rgba(200, 255, 200, 0.7)",
            "text_muted": "rgba(150, 255, 150, 0.5)",

            "accent": "#00ff66",
            "accent_light": "#80ffaa",
            "accent_dark": "#00cc44",
            "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, "
                              "stop:0 #00ff66, stop:0.5 #44ff88, stop:1 #88ffaa)",

            "success": "#00ffaa",
            "error": "#ff4466",
            "warning": "#ffaa00",

            "editor_bg": "#0a200a",
            "editor_fg": "#ccffcc",
            "editor_selection": "#00ff66",
            "line_numbers": "#1f3b1f",
            "current_line": "rgba(0, 255, 100, 0.1)",

            "glow": "rgba(0, 255, 100, 0.6)",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "glass": "rgba(0, 255, 0, 0.1)",
        }

    @staticmethod
    def dark_carbon():
        """Тёмный карбон"""
        return {
            "name": "Тёмный карбон",
            "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                      "stop:0 #1a1a1a, stop:0.5 #2a2a2a, stop:1 #1a1a1a)",

            "panel_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, "
                       "stop:0 rgba(40, 40, 40, 0.5), stop:1 rgba(30, 30, 30, 0.6))",
            "panel_border": "rgba(100, 150, 255, 0.3)",
            "panel_glow": "rgba(100, 150, 255, 0.2)",

            "text": "#ffffff",
            "text_secondary": "rgba(200, 200, 255, 0.7)",
            "text_muted": "rgba(150, 150, 200, 0.5)",

            "accent": "#6495ff",
            "accent_light": "#99bbff",
            "accent_dark": "#4169e1",
            "accent_gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, "
                              "stop:0 #6495ff, stop:0.5 #7aa5ff, stop:1 #99bbff)",

            "success": "#00ffaa",
            "error": "#ff4466",
            "warning": "#ffaa00",

            "editor_bg": "#1e1e1e",
            "editor_fg": "#ffffff",
            "editor_selection": "#6495ff",
            "line_numbers": "#3a3a4a",
            "current_line": "rgba(100, 150, 255, 0.1)",

            "glow": "rgba(100, 150, 255, 0.6)",
            "shadow": "rgba(0, 0, 0, 0.7)",
            "glass": "rgba(255, 255, 255, 0.05)",
        }


def apply_theme(widget, theme_name):
    """Применение ультрасовременного дизайна 2025"""
    theme = Themes.get_theme(theme_name)

    style = f"""
    /* Главное окно с глубоким космическим фоном */
    QMainWindow, QDialog {{
        background: {theme["main_bg"]};
    }}
    
    /* Все виджеты */
    QWidget {{
        color: {theme["text"]};
        font-family: 'Segoe UI', 'Inter', 'Arial', sans-serif;
    }}
    
    /* Панели с эффектом матового стекла (Glassmorphism) */
    QWidget#glassPanel {{
        background: {theme["panel_bg"]};
        border: 1px solid {theme["panel_border"]};
        border-radius: 24px;
        backdrop-filter: blur(10px);
    }}
    
    QWidget#glassPanel:hover {{
        background: {theme["panel_bg"].replace('0.4', '0.5').replace('0.5', '0.6')};
        border: 1px solid {theme["accent"]};
        box-shadow: 0 0 30px {theme["glow"]};
    }}
    
    /* Кнопки в стиле 2025 - глянцевые с градиентом */
    QPushButton {{
        background: {theme["accent_gradient"]};
        color: white;
        border: none;
        border-radius: 16px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        border-bottom: 4px solid {theme["accent_dark"]};
        border-right: 2px solid {theme["accent_dark"]};
    }}
    
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {theme["accent_light"]}, stop:0.5 {theme["accent"]}, stop:1 {theme["accent_light"]});
        border-bottom: 6px solid {theme["accent_dark"]};
        border-right: 3px solid {theme["accent_dark"]};
        margin-top: -2px;
        margin-left: -1px;
        box-shadow: 0 0 30px {theme["glow"]};
    }}
    
    QPushButton:pressed {{
        border-bottom: 2px solid {theme["accent_dark"]};
        border-right: 1px solid {theme["accent_dark"]};
        margin-top: 2px;
        margin-left: 1px;
    }}
    
    /* Кнопка удаления */
    QPushButton#dangerButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #ff5577, stop:0.5 #ff3366, stop:1 #ff1155);
        border-bottom: 4px solid #aa2244;
    }}
    
    QPushButton#dangerButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #ff7799, stop:0.5 #ff5577, stop:1 #ff3377);
        box-shadow: 0 0 30px rgba(255, 68, 102, 0.6);
    }}
    
    /* Кнопка успеха */
    QPushButton#successButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #00ffaa, stop:0.5 #00dd88, stop:1 #00bb66);
        border-bottom: 4px solid #008844;
    }}
    
    QPushButton#successButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #88ffcc, stop:0.5 #00ffaa, stop:1 #00dd99);
        box-shadow: 0 0 30px rgba(0, 255, 170, 0.5);
    }}
    
    /* Поля ввода со стеклянным эффектом */
    QLineEdit, QTextEdit, QComboBox {{
        background: {theme["panel_bg"]};
        border: 1px solid {theme["panel_border"]};
        border-radius: 16px;
        padding: 12px 16px;
        color: {theme["text"]};
        selection-background-color: {theme["accent"]};
        selection-color: white;
        font-size: 14px;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 2px solid {theme["accent"]};
        background: {theme["panel_bg"].replace('0.4', '0.5').replace('0.5', '0.6')};
        box-shadow: 0 0 25px {theme["glow"]};
    }}
    
    QLineEdit:hover, QTextEdit:hover, QComboBox:hover {{
        border: 1px solid {theme["accent_light"]};
        background: {theme["panel_bg"].replace('0.4', '0.45').replace('0.5', '0.55')};
    }}
    
    /* Выпадающий список */
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: url(down_arrow.png);
        width: 14px;
        height: 14px;
    }}
    
    QComboBox QAbstractItemView {{
        background: {theme["panel_bg"]};
        border: 1px solid {theme["accent"]};
        border-radius: 16px;
        padding: 8px;
        selection-background-color: {theme["accent"]};
        selection-color: white;
        backdrop-filter: blur(10px);
    }}
    
    /* Список сниппетов - карточки в стиле 2025 */
    QListWidget {{
        background: transparent;
        border: none;
        border-radius: 20px;
        padding: 12px;
    }}
    
    QListWidget::item {{
        background: {theme["panel_bg"]};
        border: 1px solid {theme["panel_border"]};
        border-radius: 20px;
        padding: 16px 20px;
        margin-bottom: 8px;
        border-bottom: 3px solid {theme["panel_border"]};
    }}
    
    QListWidget::item:hover {{
        background: {theme["panel_bg"].replace('0.4', '0.5').replace('0.5', '0.6')};
        border: 1px solid {theme["accent"]};
        border-bottom: 5px solid {theme["accent"]};
        margin-bottom: 6px;
        margin-top: -2px;
        box-shadow: 0 0 30px {theme["glow"]};
    }}
    
    QListWidget::item:selected {{
        background: {theme["accent_gradient"]};
        border: 1px solid {theme["accent_light"]};
        border-bottom: 5px solid {theme["accent_dark"]};
        color: white;
    }}
    
    /* Статус бар со стеклянным эффектом */
    QStatusBar {{
        background: {theme["panel_bg"]};
        border-top: 1px solid {theme["panel_border"]};
        color: {theme["text_secondary"]};
        padding: 10px 16px;
        font-size: 13px;
        border-radius: 0px 0px 24px 24px;
    }}
    
    /* Меню с современным дизайном */
    QMenuBar {{
        background: {theme["panel_bg"]};
        border-bottom: 1px solid {theme["panel_border"]};
        padding: 8px;
        border-radius: 24px 24px 0px 0px;
    }}
    
    QMenuBar::item {{
        padding: 8px 16px;
        border-radius: 12px;
        margin: 2px;
        color: {theme["text_secondary"]};
    }}
    
    QMenuBar::item:selected {{
        background: {theme["accent_gradient"]};
        color: white;
        border-bottom: 3px solid {theme["accent_dark"]};
    }}
    
    QMenu {{
        background: {theme["panel_bg"]};
        border: 1px solid {theme["accent"]};
        border-radius: 20px;
        padding: 8px;
        backdrop-filter: blur(10px);
    }}
    
    QMenu::item {{
        padding: 10px 28px;
        border-radius: 12px;
        margin: 4px;
        color: {theme["text"]};
    }}
    
    QMenu::item:selected {{
        background: {theme["accent_gradient"]};
        color: white;
        border-bottom: 3px solid {theme["accent_dark"]};
    }}
    
    /* Разделитель с неоновым эффектом */
    QSplitter::handle {{
        background: {theme["panel_border"]};
        width: 3px;
        margin: 15px 0;
        border-radius: 2px;
    }}
    
    QSplitter::handle:hover {{
        background: {theme["accent"]};
        width: 5px;
        box-shadow: 0 0 20px {theme["glow"]};
    }}
    
    /* Скроллбары с неоновой подсветкой */
    QScrollBar:vertical {{
        background: transparent;
        width: 14px;
        border-radius: 7px;
    }}
    
    QScrollBar::handle:vertical {{
        background: {theme["accent_gradient"]};
        border-radius: 7px;
        min-height: 40px;
        border-bottom: 3px solid {theme["accent_dark"]};
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {theme["accent_light"]};
        border-bottom: 5px solid {theme["accent_dark"]};
        margin-top: -2px;
        box-shadow: 0 0 20px {theme["glow"]};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    
    /* Лейблы с современным дизайном */
    QLabel {{
        color: {theme["text_secondary"]};
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 4px 0;
    }}
    
    QLabel#headerLabel {{
        color: {theme["text"]};
        font-size: 24px;
        font-weight: 700;
        text-transform: none;
        letter-spacing: -0.5px;
        background: transparent;
        padding: 12px 0;
        text-shadow: 0 0 20px {theme["glow"]};
    }}
    
    /* Группы с эффектом стекла */
    QGroupBox {{
        background: {theme["panel_bg"]};
        border: 1px solid {theme["panel_border"]};
        border-radius: 20px;
        margin-top: 20px;
        padding-top: 20px;
        backdrop-filter: blur(10px);
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 20px;
        padding: 0 12px;
        color: {theme["text_secondary"]};
        font-weight: 600;
        background: {theme["panel_bg"]};
        border-radius: 12px;
        border: 1px solid {theme["panel_border"]};
    }}
    
    /* Тултипы с неоновым эффектом */
    QToolTip {{
        background: {theme["panel_bg"]};
        color: {theme["text"]};
        border: 1px solid {theme["accent"]};
        border-radius: 12px;
        padding: 10px 16px;
        font-size: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px {theme["glow"]};
    }}
    """

    widget.setStyleSheet(style)
    return theme


def get_editor_style(theme):
    """Получить стиль для редактора кода"""
    return {
        "background": theme["editor_bg"],
        "foreground": theme["editor_fg"],
        "selection": theme["editor_selection"],
        "line_numbers": theme["line_numbers"],
        "current_line": theme["current_line"],
    }