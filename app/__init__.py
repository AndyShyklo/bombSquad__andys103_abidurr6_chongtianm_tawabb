"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-03-12
Time Spent: 3 hours
"""

from flask import Flask, render_template, url_for, session, request, redirect

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def landing_page():
    form_type = request.form.get('form_type')
    return render_template("index.html")

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

    
