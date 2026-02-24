"""
Современные стили для приложения с полупрозрачным фоном
Мягкие цвета и эффект стекла
"""

COLORS = {
    # Основные цвета - более мягкие и светлые
    "bg_primary": "rgba(25, 30, 40, 0.95)",      # Тёмно-синий с прозрачностью
    "bg_secondary": "rgba(35, 40, 55, 0.9)",     # Чуть светлее с прозрачностью
    "bg_tertiary": "rgba(45, 52, 68, 0.85)",     # Ещё светлее с прозрачностью

    # Акцентные цвета - мягкие и приятные
    "accent": "rgba(99, 102, 241, 0.9)",         # Индиго с прозрачностью
    "accent_light": "rgba(129, 140, 248, 0.9)",  # Светлый индиго
    "accent_gradient": "linear-gradient(135deg, rgba(99, 102, 241, 0.9), rgba(139, 92, 246, 0.9))",

    # Текст
    "text_primary": "#ffffff",                    # Белый текст (непрозрачный)
    "text_secondary": "rgba(200, 210, 240, 0.9)", # Светло-серый
    "text_muted": "rgba(150, 160, 190, 0.8)",     # Приглушённый

    # Цвета для кнопок
    "success": "rgba(16, 185, 129, 0.9)",         # Зелёный
    "warning": "rgba(245, 158, 11, 0.9)",         # Оранжевый
    "error": "rgba(239, 68, 68, 0.9)",            # Красный

    # Границы и стекло
    "border": "rgba(255, 255, 255, 0.12)",        # Полупрозрачная граница
    "glass_bg": "rgba(45, 52, 68, 0.6)",          # Сильный эффект стекла
    "glass_border": "rgba(255, 255, 255, 0.08)",  # Граница для стекла

    # Фоновые узоры (очень мягкие)
    "pattern_dots": "radial-gradient(circle at 25% 25%, rgba(255,255,255,0.02) 2px, transparent 2px)",
}

MAIN_STYLE = f"""
QMainWindow {{
    background: {COLORS["bg_primary"]} url('');  /* Тёмный фон с небольшой текстурой */
}}

QMainWindow::separator {{
    background: {COLORS["border"]};
}}

/* Глобальные настройки */
QWidget {{
    background-color: transparent;
    color: {COLORS["text_primary"]};
    font-family: 'Segoe UI', 'Arial', sans-serif;
}}

/* Стили для кнопок - с эффектом свечения */
QPushButton {{
    background: {COLORS["accent_gradient"]};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 13px;
    min-height: 30px;
    backdrop-filter: blur(5px);  /* Эффект размытия */
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(129, 140, 248, 0.95), stop:1 rgba(167, 139, 250, 0.95));
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
    backdrop-filter: blur(8px);
}}

QPushButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(79, 70, 229, 0.95), stop:1 rgba(124, 58, 237, 0.95));
    transform: scale(0.98);
}}

/* Кнопка удаления */
QPushButton#dangerButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(239, 68, 68, 0.9), stop:1 rgba(220, 38, 38, 0.9));
}}

QPushButton#dangerButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(248, 113, 113, 0.95), stop:1 rgba(239, 68, 68, 0.95));
}}

/* Кнопка успеха (добавление) */
QPushButton#successButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(16, 185, 129, 0.9), stop:1 rgba(5, 150, 105, 0.9));
}}

QPushButton#successButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(52, 211, 153, 0.95), stop:1 rgba(16, 185, 129, 0.95));
}}

/* Поля ввода - с эффектом стекла */
QLineEdit, QTextEdit, QComboBox {{
    background: {COLORS["glass_bg"]};
    border: 1px solid {COLORS["glass_border"]};
    border-radius: 10px;
    padding: 10px 14px;
    color: {COLORS["text_primary"]};
    font-size: 13px;
    selection-background-color: {COLORS["accent"]};
    backdrop-filter: blur(10px);
}}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border: 2px solid {COLORS["accent"]};
    background: rgba(45, 52, 68, 0.7);
    backdrop-filter: blur(12px);
}}

QLineEdit:hover, QTextEdit:hover, QComboBox:hover {{
    border: 1px solid {COLORS["accent_light"]};
    background: rgba(55, 62, 78, 0.7);
}}

/* Выпадающий список */
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
    image: url(down_arrow.png);
}}

QComboBox QAbstractItemView {{
    background: rgba(35, 40, 55, 0.95);
    border: 1px solid {COLORS["glass_border"]};
    border-radius: 10px;
    padding: 6px;
    selection-background-color: {COLORS["accent"]};
    backdrop-filter: blur(10px);
}}

/* Список сниппетов - с эффектом стекла */
QListWidget {{
    background: {COLORS["glass_bg"]};
    border: 1px solid {COLORS["glass_border"]};
    border-radius: 14px;
    padding: 10px;
    outline: none;
    backdrop-filter: blur(10px);
}}

QListWidget::item {{
    background: rgba(55, 62, 78, 0.6);
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 6px;
    color: {COLORS["text_primary"]};
    border: 1px solid transparent;
    backdrop-filter: blur(5px);
}}

QListWidget::item:hover {{
    background: rgba(75, 82, 98, 0.7);
    border: 1px solid {COLORS["accent_light"]};
    transform: translateX(4px);
}}

QListWidget::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(99, 102, 241, 0.7), stop:1 rgba(139, 92, 246, 0.7));
    color: white;
    border: none;
}}

/* Скроллбары - полупрозрачные */
QScrollBar:vertical {{
    background: transparent;
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background: rgba(150, 160, 190, 0.3);
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: rgba(150, 160, 190, 0.5);
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* Лейблы и заголовки - полупрозрачные */
QLabel {{
    color: {COLORS["text_secondary"]};
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    background: transparent;
}}

QLabel#headerLabel {{
    color: {COLORS["text_primary"]};
    font-size: 20px;
    font-weight: 600;
    text-transform: none;
    background: transparent;
    padding: 8px 0;
}}

/* Статус бар - с эффектом стекла */
QStatusBar {{
    background: rgba(25, 30, 40, 0.7);
    border-top: 1px solid {COLORS["glass_border"]};
    color: {COLORS["text_secondary"]};
    font-size: 12px;
    padding: 6px 12px;
    backdrop-filter: blur(10px);
}}

/* Меню - полупрозрачное */
QMenuBar {{
    background: rgba(25, 30, 40, 0.7);
    border-bottom: 1px solid {COLORS["glass_border"]};
    padding: 4px;
    backdrop-filter: blur(10px);
}}

QMenuBar::item {{
    background: transparent;
    padding: 8px 14px;
    border-radius: 6px;
    color: {COLORS["text_secondary"]};
}}

QMenuBar::item:selected {{
    background: rgba(99, 102, 241, 0.5);
    color: white;
}}

QMenu {{
    background: rgba(35, 40, 55, 0.95);
    border: 1px solid {COLORS["glass_border"]};
    border-radius: 10px;
    padding: 6px;
    backdrop-filter: blur(10px);
}}

QMenu::item {{
    padding: 8px 24px;
    border-radius: 6px;
    color: {COLORS["text_secondary"]};
}}

QMenu::item:selected {{
    background: rgba(99, 102, 241, 0.5);
    color: white;
}}

/* Сплиттер (разделитель) - полупрозрачный */
QSplitter::handle {{
    background: rgba(255, 255, 255, 0.1);
    width: 2px;
    margin: 8px 0;
}}

QSplitter::handle:hover {{
    background: {COLORS["accent"]};
}}

/* Тултипы (подсказки) */
QToolTip {{
    background: rgba(35, 40, 55, 0.95);
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["accent"]};
    border-radius: 8px;
    padding: 8px;
    font-size: 12px;
    backdrop-filter: blur(10px);
}}

/* Группы и карточки */
QGroupBox {{
    background: rgba(35, 40, 55, 0.5);
    border: 1px solid {COLORS["glass_border"]};
    border-radius: 14px;
    margin-top: 16px;
    padding-top: 16px;
    backdrop-filter: blur(8px);
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 10px 0 10px;
    color: {COLORS["text_secondary"]};
    background: transparent;
}}
"""

# Стиль для панелей с усиленным эффектом стекла
GLASS_PANEL_STYLE = """
QWidget#glassPanel {
    background: rgba(35, 40, 55, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    backdrop-filter: blur(12px);
}

QWidget#glassPanel:hover {
    background: rgba(40, 45, 60, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.12);
}
"""

# Анимации
ANIMATION_STYLES = """
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes glassPulse {
    0% { backdrop-filter: blur(8px); }
    50% { backdrop-filter: blur(12px); }
    100% { backdrop-filter: blur(8px); }
}

.glass-pulse {
    animation: glassPulse 3s infinite;
}
"""

# Объединяем все стили
STYLE_SHEET = MAIN_STYLE + GLASS_PANEL_STYLE + ANIMATION_STYLES