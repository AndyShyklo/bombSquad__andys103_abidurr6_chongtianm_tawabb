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
    url = "https://calendarific.p.rapidapi.com/holidays"

    querystring = {"year":"2025","country":"us"}

    headers = {
    	"x-rapidapi-key": "e78b4c63b3msh000d6b6bc207071p147822jsna5971b2d94ee",
    	"x-rapidapi-host": "calendarific.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

access_calendar()
