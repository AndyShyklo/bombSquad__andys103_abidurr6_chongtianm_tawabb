"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-12-12
Time Spent: 6 hours
"""

import sqlite3, urllib.request, json, time, sys, io, traceback, requests
from urllib.request import Request
from flask import render_template, Flask, session, request, redirect
from urllib.parse import urlencode

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_FILE="geo.db"

def createDB():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, geoid INTEGER, type TEXT, city TEXT, region TEXT, regionCode TEXT, country TEXT, countryCode TEXT, latitude FLOAT, longitude FLOAT, min_pop INTEGER)"
    #command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, region TEXT, country TEXT, latitude FLOAT, longitude FLOAT, time_zone TEXT, min_pop INTEGER, holidays TEXT, year INTEGER, month INTEGER, day INTEGER, time TEXT, temp INTEGER, forecast TEXT)"
    c.execute(command)
    db.commit()

def geodb(num):
    api_key = open("../keys/key_calendarific.txt", "r").read().strip()

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/"
    query_params = {
        "offset": num,
        "minPopulation": 1000000
    }

    urlb = f"{url}?{urlencode(query_params)}"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    request = urllib.request.Request(urlb, headers=headers)
    return(request)

def access_geodb():
    createDB()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    i = 0

    try:
        while (True):
            time.sleep(2)
            with urllib.request.urlopen(geodb(i)) as response:
                data = json.load(response)
                print(json.dumps(data, indent=2))
                print("A")
                cities = data.get("data", [])
                print(type(cities))
                print(cities)

                if not cities:
                    print("done")
                    break

                for item in cities:
                    geoid = item["id"]
                    type1 = item["type"]
                    city = item["city"]
                    print(city)
                    print(type(city))
                    try:
                        region = item["region"]
                        print(region)
                        print(type(region))
                        regionCode = item["regionCode"]
                    except Exception as b:
                        print("b error")
                    country = item["country"]
                    countryCode = item["countryCode"]
                    latitude = item["latitude"]
                    longitude = item["longitude"]
                    min_pop = item["population"] #https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
                    command = f"INSERT INTO geodb (geoid, type, city, region, regionCode, country, countryCode, latitude, longitude, min_pop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    print(command)
                    c.execute(command, (geoid, type1, city, region, regionCode, country, countryCode, latitude, longitude, min_pop))
                    db.commit()
                i += 5
    except urllib.error.HTTPError as e:
        print(f"httperror")
        print(e.read().decode())
    except urllib.error.URLError as e:
        print(f"urlerror")


    ret = c.execute("SELECT * FROM geodb")
    print(ret.fetchall())
    # createDB()
    # i = 0

    # c.execute(command)
    # db.commit()

def view_geodb():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT * FROM geodb")
    print(ret.fetchall())

def access_calendar(country, year, month, day):
    api_key = open("../keys/key_abstract.txt", "r").read().strip()

    url = "https://holidays.abstractapi.com/v1/"

    query_params = {
        "country": country,
        "year": year,
        "month": month,
        "day": day
    }

    urlb = f"{url}?api_key={api_key}&{urlencode(query_params)}"
    print(urlb)

    request = urllib.request.Request(urlb)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        print(f"error: {e.code}, {e.reason}")
        print(e.read().decode())
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")

def access_nws():
    #https://home.openweathermap.org/users/sign_up
    api_key = open("../keys/key_geodb.txt", "r").read().strip()

    url = "https://national-weather-service.p.rapidapi.com/points/{70.08},{70.08}"

    headers = {
        "X-RapidAPI-Key": api_key,
	    "X-RapidAPI-Host": "national-weather-service.p.rapidapi.com"
    }

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        print(f"error: {e.code}, {e.reason}")
        print(e.read().decode())
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")

access_calendar("US", "2024", "12", "13")
