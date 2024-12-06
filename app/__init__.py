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

@app.route('/', methods = ['GET', 'POST'])
def map_page():
    geodb_key = open("keys/key_geodb.txt", "r").read().strip().rstrip()
    if len(geodb_key) == 0:
        return "YOU MUST ADD YOUR API KEY IN keys/key_geodb.txt !!!"
    print(request.method)
    return render_template("index.html")

@app.route('/sus', methods=['POST'])
def sus():
    print(request.form.get('data'))
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()

@app.route("/calendar", methods=['GET', 'POST'])
def calendar_page():
    form_type = request.form.get('form_type')
    if form_type == 'weather':
        return(redirect(url_for('weather_page')))
    if form_type == 'home':
        return(redirect(url_for('landing_page')))
    return render_template('calendar.html')

@app.route("/weather", methods=['GET', 'POST'])
def weather_page():
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return(redirect(url_for('calendar_page')))
    return render_template('weather.html')
