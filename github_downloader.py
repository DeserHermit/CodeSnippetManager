"""
Скрипт для скачивания проекта с GitHub без Git
"""

import os
import zipfile
import urllib.request
import tempfile
import shutil


def download_github_repo():
    """Скачивает ZIP с GitHub и распаковывает"""

    print("=" * 50)
    print("   Скачивание Code Snippet Manager с GitHub")
    print("=" * 50)
    print()

    # URL для скачивания ZIP
    url = "https://github.com/DeserHermit/CodeSnippetManager/archive/refs/heads/master.zip"

    # Куда сохранять
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    target_dir = os.path.join(desktop, "CodeSnippetManager")

    print(f"📥 Скачиваю проект...")

    try:
        # Создаём временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            # Скачиваем
            urllib.request.urlretrieve(url, tmp_file.name)
            print(f"✅ Скачано: {tmp_file.name}")

            # Распаковываем
            print(f"📦 Распаковываю в: {target_dir}")

            with zipfile.ZipFile(tmp_file.name, 'r') as zip_ref:
                # Извлекаем все файлы
                zip_ref.extractall(desktop)

            # Переименовываем папку
            extracted_dir = os.path.join(desktop, "CodeSnippetManager-master")
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.rename(extracted_dir, target_dir)

            # Удаляем временный файл
            os.unlink(tmp_file.name)

        print(f"\n✅ Проект успешно скачан!")
        print(f"📁 Папка: {target_dir}")
        print(f"\nДля запуска:")
        print(f"1. Откройте терминал в папке: cd {target_dir}")
        print(f"2. Установите зависимости: pip install -r requirements.txt")
        print(f"3. Запустите: python main.py")

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("\nПопробуйте скачать вручную:")
        print("1. Перейдите по ссылке: https://github.com/DeserHermit/CodeSnippetManager")
        print("2. Нажмите зеленую кнопку 'Code'")
        print("3. Выберите 'Download ZIP'")
        print("4. Распакуйте архив")


if __name__ == "__main__":
    download_github_repo()
    input("\nНажмите Enter для выхода...")