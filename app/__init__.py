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
