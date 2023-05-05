import csv
import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from loguru import logger


class Command(BaseCommand):
    help = "Fills DB with data from .csv files"

    FILE_DB_TABLE: dict = {
        "category.csv": "reviews_category",
        "comments.csv": "reviews_comment",
        "genre.csv": "reviews_genre",
        "genre_title.csv": "reviews_title_genre",
        "review.csv": "reviews_review",
        "titles.csv": "reviews_title",
        "users.csv": "users_user",
    }
    DB_PATH: Path = settings.DATABASES["default"]["NAME"]

    def handle(self, *args, **options):
        logger.info("Starting...")
        csv_root: Path = settings.BASE_DIR / "static" / "data"
        files_paths = list(csv_root.glob("*.csv"))
        for file_path in files_paths:
            self.write_to_db(file_path)
        logger.info("Finished!")

    def write_to_db(self, file_path: Path) -> None:
        """Основная функция команды "manage.py take_my_db".
        1) Принимает путь к файлу .csv
        2) Устанавливает соединение с БД
        3) Открывает файл и создает список с данными для записи в
        соответствующую файлу таблицу и записывает данные в БД
        4) Закрывает соединение с БД
        5) Логирует события levels: info & critical
        """
        first_el: int = 0
        connection = sqlite3.connect(self.DB_PATH)
        try:
            logger.info(f"Starting import data from {file_path.name}")
            cursor = connection.cursor()

            with open(file_path, newline="", encoding="utf-8") as csv_file:
                dict_reader = csv.DictReader(csv_file)
                to_db = [i for i in dict_reader]

            table_keys = to_db[first_el].keys()
            values_query = self.make_values_query(table_keys)
            current_table = self.FILE_DB_TABLE[file_path.name]
            table_fields = ", ".join(table_keys)

            cursor.executemany(
                (
                    f"INSERT INTO {current_table}({table_fields}) "
                    f"VALUES ({values_query});"
                ),
                to_db,
            )
            connection.commit()
            logger.info(f"Finished import data from {file_path.name}")
        except Exception as er:
            logger.critical(f"Error: {er}")
        finally:
            connection.close()

    @staticmethod
    def make_values_query(table_keys: dict.keys) -> str:
        """Возвращает отформатированную строку.
        Пример: ":id, :username, :bio, :first_name, :last_name".
        """
        last_two: int = -2
        result = ""
        for key in table_keys:
            result += f":{key}, "
        return result[:last_two]
