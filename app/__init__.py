"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-03-12
Time Spent: 3 hours
"""

from flask import Flask, render_template, url_for, session, request, redirect

app = Flask(__name__)

@app.route("/calendar", methods=['GET', 'POST'])
def calendar_page():
    return render_template('calendar.html')

@app.route("/weather", methods=['GET', 'POST'])
def weather_page():
    return render_template('weather.html')

    
