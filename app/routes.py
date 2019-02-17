from app import app
from flask import request, render_template
from web_scraper import WebScraper
from datetime import datetime
import os

min_year = 2012
max_year = datetime.now().year

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        year = request.form['year']

        ws = WebScraper()
        terms = ws.get_courses(year)

        if int(year) >= min_year and int(year) <= max_year:
            return render_template('courses.html', terms=terms)

    return render_template('index.html')
