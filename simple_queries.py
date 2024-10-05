import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()
SERVER = os.getenv('MS_SQL_SERVER')
DATABASE = os.getenv('MS_SQL_DATABASE')
USER = os.getenv('MS_SQL_USER')
PASSWORD = os.getenv('MS_SQL_KEY')

# Строка подключения с использованием SQL Server Authentication
connectionString = f'''DRIVER={{ODBC Driver 17 for SQL Server}};
                       SERVER={SERVER};
                       DATABASE={DATABASE};
                       USER={USER};
                       PASSWORD={PASSWORD}'''
SQL_QUERY = r"""
CREATE TABLE dbo.TestTable
(id int PRIMARY KEY,
TestColum1 nvarchar(50),
TestColum2 nvarchar(100));"""

conn = pyodbc.connect(connectionString)
cursor = conn.cursor()
result = cursor.execute(SQL_QUERY)
cursor.commit()

# print(result)
# records = result.fetchall()
# print(records)
# for record in records:
#     print(f"{record.FullName}\t{record.City}")
