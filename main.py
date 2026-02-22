#!/usr/bin/env python3
"""
Code Snippet Manager - Главный файл запуска
Разработано для PyCharm
"""

import sys
import os

# Добавляем путь к нашим модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Точка входа в приложение"""
    # Создаём экземпляр приложения
    app = QApplication(sys.argv)
    app.setApplicationName("Code Snippet Manager")
    app.setOrganizationName("MyDev")

    # Создаём и показываем главное окно
    window = MainWindow()
    window.show()

    # Запускаем основной цикл приложения
    sys.exit(app.exec())


if __name__ == "__main__":
    # Этот блок выполнится только при прямом запуске файла
    print("Запуск Code Snippet Manager...")
    main()