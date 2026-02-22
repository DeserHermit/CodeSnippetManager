# -*- mode: python ; coding: utf-8 -*-

# Этот файл нужен для сборки приложения в .exe
# Он говорит PyInstaller, как собирать твою программу

import os
from PyInstaller.utils.hooks import collect_all

# Настройки для PyInstaller
block_cipher = None

# Какие дополнительные файлы включить в сборку
datas = []

# Какие модули нужно включить (PyInstaller иногда их не находит)
hiddenimports = [
    'pygments',
    'pygments.lexers',
    'pygments.formatters',
    'pygments.styles',
    'sqlite3',
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
]

# Собираем всё из PyQt6
def get_pyqt6_files():
    """Собирает все необходимые файлы PyQt6"""
    pyqt6_files = []
    for module in ['Qt6Core', 'Qt6Gui', 'Qt6Widgets']:
        try:
            files = collect_all(f'PyQt6.{module}')
            for file_type, file_list in files:
                if file_type == 'datas':
                    pyqt6_files.extend(file_list)
        except:
            pass
    return pyqt6_files

# Основной анализ проекта
a = Analysis(
    ['main.py'],  # Главный файл для запуска
    pathex=[],  # Дополнительные пути для поиска модулей
    binaries=[],  # Дополнительные бинарные файлы (DLL)
    datas=datas + get_pyqt6_files(),  # Все файлы данных
    hiddenimports=hiddenimports,  # Скрытые импорты
    hookspath=[],  # Пути к хукам
    hooksconfig={},  # Конфигурация хуков
    runtime_hooks=[],  # Хуки времени выполнения
    excludes=[],  # Что исключить из сборки
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Создаём архив Python
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Настройка исполняемого файла (.exe)
exe = EXE(
    pyz,  # Архив Python
    a.scripts,  # Скрипты
    a.binaries,  # Библиотеки
    a.datas,  # Файлы данных
    [],
    name='CodeSnippetManager',  # Имя .exe файла
    debug=False,  # Отладка (False для релиза)
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Сжатие исполняемого файла
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Не показывать консоль (True - показывать)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,  # Иконка приложения
)

# Если хочешь собрать в ОДНУ ПАПКУ (рекомендую для начала)
coll = COLLECT(
    exe,  # Исполняемый файл
    a.binaries,  # Библиотеки
    a.datas,  # Файлы данных
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CodeSnippetManager_Folder',  # Имя папки
)