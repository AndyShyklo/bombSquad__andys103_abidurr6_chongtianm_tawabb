"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-05-12
Time Spent: 3 hours
"""

import sqlite3

DB_FILE="geo.db"

def createDB():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, region TEXT, country TEXT, latitude FLOAT, longitude FLOAT, time_zone TEXT, min_pop INTEGER, holidays TEXT, year INTEGER, month INTEGER, day INTEGER, time TEXT, temp INTEGER, forecast TEXT)"
    c.execute(command)
