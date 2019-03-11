from app import app
from flask import request, render_template
from . import webscraper
from datetime import datetime
import os

min_year = 2012
max_year = datetime.now().year

@app.route('/', methods=['GET','POST'])
def light():
    return index(False)

@app.route('/dark', methods=['GET','POST'])
def dark():
    return index(True)

def index(dark_theme=False):
    if request.method == 'POST':
        year = request.form['year']

        if int(year) >= min_year and int(year) <= max_year:
            ws = webscraper.WebScraper()
            terms = ws.get_courses(year)

            return render_template('courses.html', terms=terms, url=ws.url, dark_theme=dark_theme)

    return render_template('index.html', dark_theme=dark_theme)
