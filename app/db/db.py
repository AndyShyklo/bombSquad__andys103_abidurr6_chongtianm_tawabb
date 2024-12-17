"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-12-12
Time Spent: 6 hours
"""

import sqlite3, urllib.request, json, time, sys, io, random
from urllib.request import Request
from flask import render_template, Flask, session, request, redirect
from datetime import datetime
from urllib.parse import urlencode, quote

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_FILE="geo.db"

def createDB():
    print("createDB")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, geoid INTEGER, type TEXT, city TEXT, region TEXT, regionCode TEXT, country TEXT, countryCode TEXT, latitude FLOAT, longitude FLOAT, min_pop INTEGER)"
    #command = "CREATE TABLE IF NOT EXISTS geodb (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, region TEXT, country TEXT, latitude FLOAT, longitude FLOAT, time_zone TEXT, min_pop INTEGER, holidays TEXT, year INTEGER, month INTEGER, day INTEGER, time TEXT, temp INTEGER, forecast TEXT)"
    c.execute(command)
    db.commit()

def geodb(num):
    print("geodb")
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

def DONTTOUCHaccess_geodb():
    print("DONTTOUCHaccess_geodb")
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
    print("view_geodb")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT * FROM geodb")
    print(ret.fetchall())

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
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")

def access_unsplash(query):
    print("access_unsplash")
    api_key = open("../keys/key_unsplash.txt", "r").read().strip()

    url = "https://api.unsplash.com/search/photos?client_id="

    #urlb = f"{url}lat={lat}&lon={lon}&appid={api_key}"

    urlb = f"{url}{api_key}&page=1&query={quote(query)}"

    request = urllib.request.Request(urlb)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)
            print(json.dumps(data, indent=2))
            return(data)
    except urllib.error.HTTPError as e:
        print(f"error: {e.code}, {e.reason}")
        print(e.read().decode())
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")

def find_holidays_today(countryCode):
    print("find_holidays_today")
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    print(year)
    print(month)
    print(day)
    return(access_calendar(countryCode, year, month, day))

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

def find_most_holidays(year, month, day):
    print("find_most_holidays")
    countries = get_countries()
    holis = {}

    for country in countries:
        try:
            num_holi = len(access_calendar(country, year, month, day))
        except Exception as e:
            print("Quota reached/other error")
            break
        holis[country] = num_holi
        time.sleep(2)

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

def amount_celebrating(country):
    print("amount_celebrating")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT SUM(min_pop) as total_pop FROM geodb WHERE countryCode = ?", (country,))
    pop = ret.fetchall()

    print(country + " : " + str(pop[0][0]))

    return(int(pop[0][0])) if pop[0][0] else 0

def randomize_cities(country):
    print("randomize_cities")
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    ret = c.execute("SELECT * FROM geodb WHERE countryCode = ?", (country,))
    pop = ret.fetchall()

    city = random.choice(pop)

    return(city)

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

def calculate(year, month, day):
    print("calculate")
    ans = find_most_holidays(year, month, day)
    holis = ans[0]
    holiBool = ans[1]
    holisScore = {}
    totalScore = 0

    #if holidays exist (likely)
    if holiBool == True:
        for key, value in holis.items():
            if value == 1:
                holisScore[key] = value * amount_celebrating(key) * 2
            elif value == 2:
                holisScore[key] = value * amount_celebrating(key) * 6
            elif value >= 3:
                holisScore[key] = value * amount_celebrating(key) * 10
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

def total_info(year, month, day):
    # ans = [(1782, 118499, 'CITY', 'Houston', 'Texas', 'TX', 'United States of America', 'US', 29.762777777, -95.383055555, 2304580), 10000, 100000]
    ans = calculate(year, month, day)
    city = ans[0]
    city += (ans[1]),
    city += (ans[2]),
    city += (amount_celebrating(city[7])),
    city += (year),
    city += (month),
    city += (day),
    e = access_calendar(city[7], 2024, 12, 15)
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
    data = access_unsplash(city[3])
    city += (data["results"][0]["urls"]["full"]),
    city += (data["results"][0]["alt_description"]),
    city += (data["results"][0]["user"]["first_name"] + " " + data["results"][0]["user"]["last_name"]),

    print(city)
    createTotalDB()
    viewCity()
    insertCity(city)
    viewCity()

def createTotalDB():
    DB2_FILE="total.db"

    print("createDB2")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS total (id INTEGER, geoid INTEGER, type TEXT, city TEXT, region TEXT, regionCode TEXT, country TEXT, countryCode TEXT, latitude FLOAT, longitude FLOAT, min_pop INTEGER, score INTEGER, total_score INTEGER, country_pop INTEGER, year INTEGER, month INTEGER, day INTEGER, num_holidays INTEGER, holidays TEXT, holidays_desc TEXT, image TEXT, image_desc TEXT, image_author TEXT)"
    c.execute(command)
    db.commit()
    db.close()

def passInfo(year, month, day):
    #[city, country, longitude, latitude, image, image_desc, image_author, [holiday1, holiday2, ...]]
    DB2_FILE="total.db"

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
        return("Error, date not in database")
    

def insertCity(city):
    DB2_FILE="total.db"

    print("insertCity")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()
    com = c.execute("SELECT * FROM total WHERE year = ? AND month = ? AND day = ?", (city[14], city[15], city[16],))
    pop2 = com.fetchall()
    print(type(pop2))
    if pop2:
        print("Error: duplicate date")
    else:
        command = f"INSERT INTO total (id, geoid, type, city, region, regionCode, country, countryCode, latitude, longitude, min_pop, score, total_score, country_pop, year, month, day, num_holidays, holidays, holidays_desc, image, image_desc, image_author) VALUES {city}"
        c.execute(command)
        db.commit()
        print("City inserted successfully")
    db.close()

def viewCity():
    DB2_FILE="total.db"

    print("viewCity")
    db = sqlite3.connect(DB2_FILE)
    c = db.cursor()

    ret = c.execute("SELECT * FROM total")
    print(ret.fetchall())
    return(ret.fetchall())

# access_calendar("US", "2024", "12", "13")
# time.sleep(2)
# print("space")
# find_holidays_today("US")

# print("hi")

#access_unsplash("Antarctica")
#find_most_holidays()
# print(find_most_holidays())

# print(calculate())
# print(total_info(2024, 12, 16))

# city = (1782, 118499, 'CITY', 'Houston', 'Texas', 'TX', 'United States of America', 'US', 29.762777777, -95.383055555, 2304580)
# print(access_calendar(city[7], 2024, 12, 31))
# data = access_unsplash("Khartoum Bahri")
# print(data["results"][0]["urls"]["full"])
# print(data["results"][0]["alt_description"])
# print(data["results"][0]["user"]["first_name"] + data["results"][0]["user"]["last_name"])

# passInfo(2024, 12, 15)
