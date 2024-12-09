"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-05-12
Time Spent: 3 hours
"""

import sqlite3, requests

DB_FILE="geo.db"

def createDB():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, region TEXT, country TEXT, latitude FLOAT, longitude FLOAT, time_zone TEXT, min_pop INTEGER, holidays TEXT, year INTEGER, month INTEGER, day INTEGER, time TEXT, temp INTEGER, forecast TEXT)"
    c.execute(command)

def access_calendar():
    cal_key = open("../keys/key_calendarific.txt", "r").read().strip().rstrip()
    url = f"https://calendarific.p.rapidapi.com/holidays?={cal_key}"

    querystring = {"year":"2019","country":"US"}

    response = requests.get(url, params=querystring)

    print(response.json())

access_calendar()
