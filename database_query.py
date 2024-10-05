import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()
SERVER = os.getenv('MS_SQL_SERVER')
DATABASE = os.getenv('MS_SQL_DATABASE')
USER = os.getenv('MS_SQL_USER')
PASSWORD = os.getenv('MS_SQL_KEY')

# Создаем строку подключения
connection_string = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};USER={USER};PASSWORD={PASSWORD}'

# Устанавливаем соединение
try:
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    print("Подключение успешно!")
except Exception as e:
    print(f"Ошибка подключения: {e}")

# Создание Базы данных
try:
    SQL_QUERY = """CREATE DATABASE TestDB;
GO"""
    print("База данных создана!")
except Exception as e:
    print(f"Ошибка при создании базы данных: {e}")

# Создание таблицы
try:
    SQL_QUERY = """CREATE TABLE Users (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50),
    Age INT
);
GO"""
    print("Таблица создана!")
except Exception as e:
    print(f"Ошибка при создании таблицы: {e}")

# Заполнение таблицы данными
try:
    SQL_QUERY = """INSERT INTO Users (Name, Age) VALUES ('Иван', 30);
INSERT INTO Users (Name, Age) VALUES ('Анна', 25);
GO"""
    print("Данные добавлены в таблицу!")
except Exception as e:
    print(f"Ошибка при добавлении данных: {e}")

# Вывод данных из базы данных
try:
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()

    users_list = []
    for row in rows:
        users_list.append({'ID': row.ID, 'Name': row.Name, 'Age': row.Age})

    print("Данные из таблицы:", users_list)
except Exception as e:
    print(f"Ошибка при выводе данных: {e}")