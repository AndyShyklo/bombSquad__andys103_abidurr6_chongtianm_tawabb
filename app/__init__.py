
"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-03-12
Time Spent: 3 hours
"""

from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3, urllib.request, urllib.parse, json


app = Flask(__name__)

def get_coord(long, lat):
    return [(1.3) * long / 2 - 75, -lat / 2 - 30]

@app.route('/', methods = ['GET', 'POST'])
def map_page():
    '''
    try:
        geodb_key = open("keys/key_geodb.txt", "r").read().strip().rstrip()
        #print(geodb_key)
    except:
        return "YOU MUST CREATE A keys/key_geodb.txt FILE AND STORE YOUR API KEY IN IT!!"
    if len(geodb_key) == 0:
        return "YOU MUST ADD YOUR API KEY IN keys/key_geodb.txt !!!"
    '''
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return(redirect(url_for('calendar_page')))

    # -95
    # longitude = (1.3) * -95/2 -75 # range [-180, 180]
    # latitude = -35.8/2 -30 # range [-90, 90]
    longitude, latitude = get_coord(-98.3, 38.5)
    day = "Initial Setup"
    return render_template('index.html', longitude = (longitude + 180) / 360, latitude = (latitude + 90) / 180, day = day)

@app.route('/day/<day>')
def map_day(day):
   return "hi" 

@app.route("/calendar", methods=['GET', 'POST'])
def calendar_page():
    form_type = request.form.get('form_type')
    if form_type == 'weather':
        return(redirect(url_for('weather_page')))
    if form_type == 'home':
        return(redirect(url_for('map_page')))
    return render_template('calendar.html')

@app.route("/weather", methods=['GET', 'POST'])
def weather_page():
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return(redirect(url_for('calendar_page')))
    return render_template('weather.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
