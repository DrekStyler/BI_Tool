import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()

    c.execute("""CREATE TABLE companies
    (company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, revenue INTEGER NOT NULL)""")

    c.execute('INSERT INTO companies (name, revenue)'
    'VALUES("Apple",1000000)')
