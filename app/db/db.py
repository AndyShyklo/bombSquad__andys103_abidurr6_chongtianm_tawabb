"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-12-17
Time Spent: 15 hours
"""

import time, sys, io, random
from math import log
from datetime import datetime
import sqlite3, urllib.request, json
from urllib.parse import urlencode, quote
from flask import render_template, Flask, session, request, redirect
from urllib.request import Request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_FILE="geo.db"

#db is present, not needed
def createDB():
    print("createDB")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, geoid INTEGER, type TEXT, city TEXT, region TEXT, regionCode TEXT, country TEXT, countryCode TEXT, latitude FLOAT, longitude FLOAT, min_pop INTEGER)"
    #command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, region TEXT, country TEXT, latitude FLOAT, longitude FLOAT, time_zone TEXT, min_pop INTEGER, holidays TEXT, year INTEGER, month INTEGER, day INTEGER, time TEXT, temp INTEGER, forecast TEXT)"
    c.execute(command)
    db.commit()

#access for geo_db
def access_geodb(num):
    print("access_geodb")
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

#do not run, recreates entire geo.db database for ~25 minutes
def populate_geodb():
    print("populate_geodb")
    createDB()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    i = 0

    try:
        c.execute("DELETE FROM geodb")
        while (True):
            time.sleep(2)
            with urllib.request.urlopen(access_geodb(i)) as response:
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
                    min_pop = item["population"] 
                    command = "INSERT INTO geodb (geoid, type, city, region, regionCode, country, countryCode, latitude, longitude, min_pop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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

#views geodb table
def view_geodb():
    print("view_geodb")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT * FROM geodb")
    print(ret.fetchall())

#accesses abstract api
def access_calendar(country, year, month, day):
    print("access_calendar")
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
            return(data)
    except urllib.error.HTTPError as e:
        print(f"error: {e.code}, {e.reason}")
        print(e.read().decode())
        return(-1)
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")
        return(-1)
    except Exception as e:
        print(f"auth error: {e}")
        return(-1)

#accesses unsplash api
def access_unsplash(query):
    print("access_unsplash")
    api_key = open("../keys/key_unsplash.txt", "r").read().strip()

    url = "https://api.unsplash.com/search/photos?client_id="

    print("quote query:" + quote(query))
    print("query:" + query)

    urlb = f"{url}{api_key}&page=1&query={quote(query)}"
    print(urlb)

    request = urllib.request.Request(urlb)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
            # print(json.dumps(data, indent=2))
            return(data)
    except urllib.error.HTTPError as e:
        print(f"error: {e.code}, {e.reason}")
        print(e.read().decode())
        return(-1)
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")
        return(-1)

#not needed anymore, finds todays holidays
def find_holidays_today(countryCode):
    print("find_holidays_today")
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    print(year)
    print(month)
    print(day)
    return(access_calendar(countryCode, year, month, day))

#gets a list of all holidays in geodb (with cities over 1 million people)
def get_countries():
    print("get_countries")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT countryCode FROM geodb")
    retc = ret.fetchall()

    print(retc)

    list1 = []

    for item in (retc):
        str = ''.join(item)
        if str not in list1:
            list1.append(str)

    return(list1)

#not needed anymore, finds most holidays today
def find_most_holidays_today():
    print("find_most_holidays_today")
    countries = get_countries()
    holis = {}

    for country in countries:
        num_holi = len(find_holidays_today(country))
        holis[country] = num_holi
        time.sleep(1.1)

    print(holis)
    print("space")

    holis2 = {}

    for key, value in holis.items():
        if value > 0:
            holis2[key] = value

    print(holis2)
    return(holis2)

#finds most holidays on a given day
def find_most_holidays(year, month, day):
    print("find_most_holidays")
    countries = get_countries()
    holis = {}

    i = 0

    for country in countries:
        i += 1
        try:
            a = access_calendar(country, year, month, day)
            if a == -1:
                print("Error")
                return(-1)
            num_holi = len(a)
            print(i)
            print(country)
        except Exception as e:
            print("Quota reached/other error")
            print("Stopped on country " + str(country))
            print(i)
            print(country)
            return(-1)
        holis[country] = num_holi
        time.sleep(1.1)

    print(f"num of iterations {i}")

    print(holis)
    print("space")

    holis2 = {}

    for key, value in holis.items():
        if value > 0:
            holis2[key] = value

    if len(holis2) == 0:
        return([holis, False])

    print(holis2)
    return([holis2, True])

#finds total population of country based on biggest cities
def amount_celebrating(country):
    print("amount_celebrating")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT SUM(min_pop) as total_pop FROM geodb WHERE countryCode = ?", (country,))
    pop = ret.fetchall()

    print(country + " : " + str(pop[0][0]))

    return(int(pop[0][0])) if pop[0][0] else 0

#randomizes cities within a country
def randomize_cities(country):
    print("randomize_cities")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT * FROM geodb WHERE countryCode = ?", (country,))
    pop = ret.fetchall()

    city = random.choice(pop)

    return(city)

#randomizes country based on weights and factors like holiday amount and population
def randomize_country(holisScore, totalScore):
    print("randomize_country")
    weights = {}
    for key, value in holisScore.items():
        weights[key] = value/totalScore

    selected_item = random.choices(population=list(weights.keys()), weights=(weights.values()), k=1)

    print(weights)
    print(selected_item)
    print(selected_item[0])
    print(weights[selected_item[0]])
    return(selected_item[0])

#calculates a basic score, that is then sent to a randomizer
def calculate(year, month, day):
    print("calculate")
    ans = find_most_holidays(year, month, day)
    if ans == -1:
        print("Error")
        return(-1)
    holis = ans[0]
    holiBool = ans[1]
    holisScore = {}
    totalScore = 0

    #if holidays exist (likely)
    if holiBool == True:
        for key, value in holis.items():
            if value == 1:
                holisScore[key] = value * log(amount_celebrating(key)) * 2
            elif value == 2:
                holisScore[key] = value * log(amount_celebrating(key)) * 6
            elif value >= 3:
                holisScore[key] = value * log(amount_celebrating(key)) * 10
            totalScore += holisScore[key]

    #if they dont exist (unlikely/impossible)
    elif holiBool == False:
        for key, value in holis:
            holisScore[key] = value * amount_celebrating(key) * 2
            totalScore += holisScore[key]

    print("holiScore:")
    print(holisScore)
    print("totalScore: " + str(totalScore))

    if totalScore == 0:
        return("Error, totalScore = 0")

    country = randomize_country(holisScore, totalScore)
    city = randomize_cities(country)

    return([city, holisScore[country], totalScore])

#the main parent function, formats and returns all information
def total_info(year, month, day):
    # ans = [(1782, 118499, 'CITY', 'Houston', 'Texas', 'TX', 'United States of America', 'US', 29.762777777, -95.383055555, 2304580), 10000, 100000]
    DB2_FILE="total.db"

    print("total_info")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()
    com = c.execute("SELECT * FROM total WHERE year = ? AND month = ? AND day = ?", (year, month, day,))
    pop2 = com.fetchall()
    print(type(pop2))
    if pop2:
        print("Error: duplicate date")
        return("Error: duplicate date")
    else:
        print("good date")
        ans = calculate(year, month, day)
        if ans == -1:
            return("Error")
        city = ans[0]
        city += (ans[1]),
        city += (ans[2]),
        city += (amount_celebrating(city[7])),
        city += (year),
        city += (month),
        city += (day),
        e = access_calendar(city[7], year, month, day)
        arr = []
        i = 0
        for item in e:
            arr.append(item["name"])
            i += 1
        city += (i),
        jdata = json.dumps(arr)
        city += (jdata),
        arr2 = []
        for item in e:
            arr2.append(item["description"])
        jdata2 = json.dumps(arr2)
        city += (jdata2),
        data = access_unsplash(city[3])["results"]
        if len(data) > 0:
            datab = random.choice(data)
        else:
            data = access_unsplash(city[6])["results"]
            if len(data) > 0:
                datab = random.choice(data)
            else:
                print("error")
                datab = "error"
        print(datab)
        print("space")

        city += (datab["urls"]["full"]),
        city += (datab["alt_description"]),
        city += (str(datab["user"]["first_name"]) + " " + str(datab["user"]["last_name"])),

        time.sleep(2)

        print(city)
        createTotalDB()
        viewCity()
        insertCity(city)
        viewCity()

#creates total locations db
def createTotalDB():
    DB2_FILE="total.db"

    print("createDB2")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS total (id INTEGER, geoid INTEGER, type TEXT, city TEXT, region TEXT, regionCode TEXT, country TEXT, countryCode TEXT, latitude FLOAT, longitude FLOAT, min_pop INTEGER, score INTEGER, total_score INTEGER, country_pop INTEGER, year INTEGER, month INTEGER, day INTEGER, num_holidays INTEGER, holidays TEXT, holidays_desc TEXT, image TEXT, image_desc TEXT, image_author TEXT)"
    c.execute(command)
    db.commit()
    db.close()

#passes info in a usable manner to front end
def passInfo(year, month, day):
    #[city, country, longitude, latitude, image, image_desc, image_author, [holiday1, holiday2, ...]]
    DB2_FILE="db/total.db"
    #import os
    # print("Using database file:", os.path.abspath(DB2_FILE))

    print("passInfo")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()

    ret = c.execute("SELECT city, country, longitude, latitude, image, image_desc, image_author, holidays FROM total WHERE year = ? AND month = ? AND day = ?", (year, month, day,))
    oeo = ret.fetchall()
    if oeo:
        sevenT = json.loads(oeo[0][7])

        arr = [oeo[0][0], oeo[0][1], oeo[0][2], oeo[0][3], oeo[0][4], oeo[0][5], oeo[0][6], sevenT]
        print(arr)
        return(arr)
    else:
        print("Error, date not in database")
        return(-1)
    
#inserts city data for the day into total db
def insertCity(city):
    DB2_FILE="total.db"

    print("insertCity")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()
    try:
        com = c.execute("SELECT * FROM total WHERE year = ? AND month = ? AND day = ?", (city[14], city[15], city[16],))
        pop2 = com.fetchall()
        print(type(pop2))
        if pop2:
            print("Error: duplicate date")
        else:
            command = "INSERT INTO total (id, geoid, type, city, region, regionCode, country, countryCode, latitude, longitude, min_pop, score, total_score, country_pop, year, month, day, num_holidays, holidays, holidays_desc, image, image_desc, image_author) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            c.execute(command, city)
            db.commit()
            print("City inserted successfully")
    except sqlite3.Error as e:
        print(f"Error adding: {e}")
    db.close()

#views the total db
def viewCity():
    DB2_FILE="total.db"

    print("viewCity")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()

    ret = c.execute("SELECT * FROM total")
    print(ret.fetchall())
    return(ret.fetchall())

#removes a row from the total db
def removeCity(year, month, day):
    DB2_FILE = "total.db"

    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()

    try:
        c.execute("DELETE FROM total WHERE year = ? AND month = ? AND day = ?",(year, month, day))
        db.commit()

        if c.rowcount > 0:
            print(f"removed from {year}, {month}, {day}")
        else:
            print(f"nothing to delete for {year}, {month}, {day}")
    except sqlite3.Error as e:
        print(f"error for: {e}")
    finally:
        db.close()

#gets the days that were used in total db in an accessible manner for front end
def getDays():
    DB2_FILE="total.db"

    print("getDays")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()

    ret = c.execute("SELECT year, month, day FROM total")

    print(ret.fetchall())
    return(ret.fetchall())

