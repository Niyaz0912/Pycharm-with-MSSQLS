import os
from dotenv import load_dotenv
import pyodbc
import json
from datetime import datetime

load_dotenv()
SERVER = os.getenv('MS_SQL_SERVER')
DATABASE = os.getenv('MS_SQL_DATABASE')
USER = os.getenv('MS_SQL_USER')
PASSWORD = os.getenv('MS_SQL_KEY')

print(f"Connecting to {SERVER} database {DATABASE} with user {USER}")

# Строка подключения к SQL Server
connectionString = f'''
    DRIVER={{ODBC Driver 17 for SQL Server}};
    SERVER={SERVER};
    DATABASE={DATABASE};
    UID={USER};
    PWD={PASSWORD}
'''


class Database:
    """Класс для управления подключением к базе данных SQL Server."""

    def __init__(self, server, database, username, password):
        """
        Инициализация соединения с базой данных.

        :param server: Адрес сервера базы данных.
        :param database: Имя базы данных.
        :param username: Имя пользователя для подключения.
        :param password: Пароль для подключения.
        """
        self.connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        self.cursor = self.connection.cursor()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()


class ProductsDatabase(Database):
    """Класс для выполнения запросов к таблице Products в базе данных."""

    def query_exists_fruits(self):
        """
        Запрос для проверки существования фруктов в таблице Products.

        :return: SQL-запрос как строка.
        """
        return '''
            SELECT * FROM Products 
            WHERE EXISTS (
                SELECT 1 FROM Products WHERE type = 'fruit' AND id = Products.id
            )
        '''

    # Другие методы...

    def fetch_all_results(self, query):
        """
        Выполняет SQL-запрос и возвращает результаты в виде списка словарей.

        :param query: SQL-запрос как строка.
        :return: Список словарей с результатами запроса.
        """
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


def serialize_datetime(obj):
    """
    Сериализация объектов datetime в ISO формат.

    :param obj: Объект для сериализации.
    :return: Строка в формате ISO 8601, если объект является datetime.
    :raises TypeError: Если объект не является сериализуемым типом.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()  # Преобразует datetime в строку ISO 8601
    raise TypeError("Type not serializable")


def save_to_json(data, filename):
    """
    Сохраняет данные в JSON файл.

    :param data: Данные для сохранения (обычно словарь).
    :param filename: Имя файла, в который будут сохранены данные.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, default=serialize_datetime, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    try:
        db = ProductsDatabase(server=SERVER, database=DATABASE, username=USER, password=PASSWORD)

        results = {}

        try:
            results["Exists Fruits"] = db.fetch_all_results(db.query_exists_fruits())
            # Добавьте остальные запросы здесь...

            save_to_json(results, 'query_results.json')

        except Exception as e:
            print("Error during query execution:", e)

    except Exception as e:
        print("Error connecting to the database:", e)

    finally:
        if 'db' in locals():
            db.close()