import os
import logging
from functools import wraps


class FileNotFound(Exception):
    """Файл не знайдено"""
    pass


class FileCorrupted(Exception):
    """Файл пошкоджено або недоступний"""
    pass


def logged(mode="console"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.ERROR)

            if not logger.handlers:
                if mode == "console":
                    handler = logging.StreamHandler()
                elif mode == "file":
                    handler = logging.FileHandler("log.txt", encoding="utf-8")
                else:
                    raise ValueError("Невідомий режим логування")

                formatter = logging.Formatter(
                    "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)

            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(str(e))
                raise

        return wrapper
    return decorator


class FileManager:

    @logged("console")
    def __init__(self, file_path: str):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            try:
                with open(self.file_path, "w", encoding="utf-8"):
                    print(f"[INFO] Файл створено: {self.file_path}")
            except IOError:
                raise FileNotFound(f"Неможливо створити файл: {self.file_path}")

    @logged("file")
    def read(self) -> str:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except (IOError, OSError):
            raise FileCorrupted(f"Помилка читання або файл пошкоджено: {self.file_path}")

    @logged("file")
    def write(self, text: str):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(text)
        except (IOError, OSError):
            raise FileCorrupted(f"Запис у файл неможливий: {self.file_path}")

    @logged("file")
    def append(self, text: str):
        try:
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(text)
        except (IOError, OSError):
            raise FileCorrupted(f"Не вдалося дописати у файл: {self.file_path}")


def main():
    try:
        print("Поточна директорія:", os.getcwd())
        manager = FileManager("file.txt")

        manager.write("В мене не здано 7 лаб з фізики\n")
        manager.append("Це жах\n")

        content = manager.read()
        print("Вміст файлу:")
        print(content)

    except FileNotFound as e:
        print("ПОМИЛКА:", e)
    except FileCorrupted as e:
        print("ПОМИЛКА:", e)


if __name__ == "__main__":
    main()

