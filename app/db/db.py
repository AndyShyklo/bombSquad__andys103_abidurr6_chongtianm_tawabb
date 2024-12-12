"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-05-12
Time Spent: 3 hours
"""

import sqlite3, urllib.request, json
from flask import render_template, Flask, session, request, redirect
from urllib.parse import urlencode

DB_FILE="geo.db"

def createDB():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, geoid INTEGER, type TEXT, city TEXT, region TEXT, regionCode TEXT, country TEXT, countryCode TEXT, latitude FLOAT, longitude FLOAT, min_pop INTEGER)"
    #command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, region TEXT, country TEXT, latitude FLOAT, longitude FLOAT, time_zone TEXT, min_pop INTEGER, holidays TEXT, year INTEGER, month INTEGER, day INTEGER, time TEXT, temp INTEGER, forecast TEXT)"
    c.execute(command)
    db.commit()

def access_geodb():
    api_key = open("../keys/key_geodb.txt", "r").read().strip()

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/"
    query_params = {
        "offset": 50,
        "minPopulation": 1000000
    }

    urlb = f"{url}?{urlencode(query_params)}"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    request = urllib.request.Request(urlb, headers=headers)

    createDB()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
            print(json.dumps(data, indent=2))
            for i in range (0, 2):
                # try:
                    print("A")
                    x1 = data["data"]
                    print(type(x1))
                    print(x1)
                    for item in x1:
                        geoid = item["id"]
                        type1 = item["type"]
                        city = item["city"]
                        print(city)
                        print(type(city))
                        region = item["region"]
                        print(region)
                        print(type(region))
                        regionCode = item["regionCode"]
                        country = item["country"]
                        countryCode = item["countryCode"]
                        latitude = item["latitude"]
                        longitude = item["longitude"]
                        min_pop = item["population"] #https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
                        command = f"INSERT INTO geodb (geoid, type, city, region, regionCode, country, countryCode, latitude, longitude, min_pop) VALUES ({geoid}, {type1}, {city}, {region}, {regionCode}, {country}, {countryCode}, {latitude}, {longitude}, {min_pop})"
                        print(command)
                        c.execute(command)
                        db.commit()
                # except Exception as e:
                #     print("error")
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

def access_calendar():
    api_key = open("../keys/key_calendarific.txt", "r").read().strip()

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    query_params = {
        "countryIds": "US",
        "minPopulation": 100000
    }

    urlb = f"{url}?{urlencode(query_params)}"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    request = urllib.request.Request(urlb, headers=headers)

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
    api_key = open("../keys/key_nws.txt", "r").read().strip()

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    query_params = {
        "countryIds": "US",
        "minPopulation": 100000
    }

    urlb = f"{url}?{urlencode(query_params)}"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    request = urllib.request.Request(urlb, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        print(f"error: {e.code}, {e.reason}")
        print(e.read().decode())
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")

access_geodb()
