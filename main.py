#!/usr/bin/env python3
"""
Главный файл запуска Code Snippet Manager
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    app.setApplicationName("Code Snippet Manager")
    app.setOrganizationName("DeserHermit")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()