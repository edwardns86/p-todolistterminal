import os
import sqlite3
import datetime

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor() 

sql = """
  CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT DEFAULT "today",
    created TEXT DEFAULT "incomplete",
    )
"""
cur.execute(sql)
conn.commit()


sql = """
  CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY,
    project name TEXT NOT NULL,
    due_date DATE DEFAULT "",
    status TEXT DEFAULT "incomplete",
    )
"""
cur.execute(sql)
conn.commit()