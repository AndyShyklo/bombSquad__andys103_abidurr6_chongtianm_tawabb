"""
Bomb Squad: Andy Shyklo, Abidur Rahman, Mark Ma, Tawab Berri
SoftDev
P01: Topher Time
2024-03-12
Time Spent: 3 hours
"""

from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime
from db.db import passInfo

app = Flask(__name__)

def get_coord(long, lat):
    return [(1.3) * long / 2 - 75, -lat / 2 - 30]

@app.route('/', methods=['GET', 'POST'])
def map_page():
    longitude, latitude = get_coord(-98.3, 38.5)
    day = "Initial Setup"
    city = ""
    image_link = ""
    image_author = ""
    holidays = []

    y, m, d, = -1, -1, -1

    if request.method == "POST":
        y = request.form["year"]
        m = request.form["month"]
        d = request.form["day"]
        day = f'{m}/{d}/{y}'

    # [city, country name, longitude, latitude, image, image desc, image author, [holiday1, holiday2, ...]]
    
    if y != -1:
        #l = ['Chicago', 'US', -87.5, 41.7, "https://www.usbeacon.com/images/Illinois/maps/Chicago_o.gif", "desc", "author", ['holiday1', 'holiday2']]
        l = passInfo(y, m, d)
        longitude, latitude = get_coord(l[2], l[3])
        city = f'{l[0]}, {l[1]}'
        image_link = l[4]
        image_author = l[6]
        holidays = l[7]

    return render_template('index.html', longitude=(longitude + 180) / 360, latitude=(latitude + 90) / 180, day=day, city=city,
                           image_link = image_link,
                           image_author = image_author,
                           holidays = holidays
                           )

def calFunction(year, month):
    text_cal = calendar.HTMLCalendar(firstweekday=0)
    return text_cal.formatmonth(year, month)

@app.route("/calendar", methods=['GET', 'POST'])
def calendar_page():
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    if request.method == 'POST':
        year = int(request.form.get('year', current_year))
        month = int(request.form.get('month', current_month))

        if 'prev_month' in request.form:
            month -= 1
            if month < 1:  
                month = 12
                year -= 1  
        elif 'next_month' in request.form:
            month += 1
            if month > 12:  
                month = 1
                year += 1  
        elif 'weather' in request.form:
            print("weather")
            return redirect(url_for('weather_page'))
        elif 'home' in request.form:
            print("home")
            return redirect(url_for('map_page'))
    else:
        year = current_year
        month = current_month

    calHTML = calFunction(year, month)
    month_name = calendar.month_name[month]

    return render_template('calendar.html', calContent=calHTML, month=month, year=year, month_name=month_name)

@app.route("/weather", methods=['GET', 'POST'])
def weather_page():
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return redirect(url_for('calendar_page'))
    return render_template('weather.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
