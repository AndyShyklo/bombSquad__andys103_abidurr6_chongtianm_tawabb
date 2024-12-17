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

app = Flask(__name__)

def get_coord(long, lat):
    return [(1.3) * long / 2 - 75, -lat / 2 - 30]

@app.route('/', methods=['GET', 'POST'])
def map_page():
    print("hello")
    calDay = ""
    calMonth = ""
    calYear = ""

    longitude, latitude = get_coord(-98.3, 38.5)
    day = "Initial Setup"
    
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return redirect(url_for('calendar_page'))

    return render_template('index.html', longitude=(longitude + 180) / 360, latitude=(latitude + 90) / 180, day=day)

class CustomHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self, year, month):
        super().__init__()
        self.year = year
        self.month = month

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  
        else:
            return f'''
            <td class="day">
                <form method="POST" action="/" name="greenDay" value = "bye">
                    <input type="hidden" name="day" value="{day}">
                    <input type="hidden" name="month" value="{self.month}">
                    <input type="hidden" name="year" value="{self.year}">
                    <button type="submit" class="date-button">{day}</button>
                </form>
            </td>'''

    def formatmonth(self, year, month):
        # Call the original formatmonth to get the basic structure
        month_str = super().formatmonth(year, month)
        # Add custom CSS for styling
        custom_css = '''
        <style>
            .day {
                border: 1px solid #000; /* Box outline */
                text-align: center;
                padding: 10px;
            }
            .date-button {
                background-color: green; /* Green button */
                color: white; /* White text */
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                cursor: pointer;
            }
            .noday {
                background-color: #f0f0f0; /* Light gray for empty days */
            }
        </style>
        '''
        return custom_css + month_str

def calFunction(year, month):
    text_cal = CustomHTMLCalendar(year, month)
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
        elif 'home' in request.form:
            print("home")
            return redirect(url_for('map_page'))
        elif "greenDay" in request.form:
            print("received")
            calDay = request.form.get("day")
            calMonth = request.form.get("month")
            calYear = request.form.get("year")
            print(f"Day: {calDay}, Month: {calMonth}, Year: {calYear}")
    else:
        year = current_year
        month = current_month

    calHTML = calFunction(year, month)
    month_name = calendar.month_name[month]

    return render_template('calendar.html', calContent=calHTML, month=month, year=year, month_name=month_name)

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/weather", methods=['GET', 'POST'])
def weather_page():
    form_type = request.form.get('form_type')
    if form_type == 'calendar':
        return redirect(url_for('calendar_page'))
    return render_template('weather.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
