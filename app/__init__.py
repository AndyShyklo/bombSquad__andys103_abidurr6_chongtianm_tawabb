from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime

app = Flask(__name__)

def get_coord(long, lat):
    return [(1.3) * long / 2 - 75, -lat / 2 - 30]

@app.route('/', methods=['GET', 'POST'])
def map_page():
    longitude, latitude = get_coord(-98.3, 38.5)
    day = "Initial Setup"
    
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return redirect(url_for('calendar_page'))

    return render_template('index.html', longitude=(longitude + 180) / 360, latitude=(latitude + 90) / 180, day=day)

@app.route("/calendar", methods=['GET', 'POST'])
def calendar_page():
    
    now = datetime.now()
    month = request.args.get('month', now.month, type=int)
    year = request.args.get('year', now.year, type=int)

   
    first_day = calendar.monthrange(year, month)[0]  
    num_days = calendar.monthrange(year, month)[1]

    
    days = [day for day in range(1, num_days + 1)]

    
    weeks = []
    week = [''] * 7  

    
    for i in range(first_day):
        week[i] = ''

    
    for day in days:
        week[first_day] = day
        first_day += 1
        if first_day == 7:  
            weeks.append(week)
            week = [''] * 7
            first_day = 0

 
    if any(week):
        weeks.append(week)

    
    if request.method == 'POST':
        if 'prev_month' in request.form:
            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1
        elif 'next_month' in request.form:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1


    month_name = calendar.month_name[month]

    return render_template('calendar.html', weeks=weeks, month=month, year=year, month_name=month_name)

@app.route("/weather", methods=['GET', 'POST'])
def weather_page():
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return redirect(url_for('calendar_page'))
    return render_template('weather.html')

if __name__ == "__main__":
    app.debug = True
    app.run()