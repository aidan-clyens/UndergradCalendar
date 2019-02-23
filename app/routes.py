from app import app
from flask import request, render_template
from . import webscraper
from . import db
from datetime import datetime
import os

min_year = 2012
max_year = datetime.now().year

@app.route('/', methods=['GET','POST'])
def index():

    res = db.init_db()

    if request.method == 'POST':
        year = request.form['year']

        select_sql = """SELECT * FROM courses WHERE start_year=%s""" % year
        res = db.query_db(select_sql)
        if len(res) > 0:
            terms = db.get_courses_from_db(year)
        else:
            ws = webscraper.WebScraper()
            terms = ws.get_courses(year)

        if int(year) >= min_year and int(year) <= max_year:
            return render_template('courses.html', terms=terms)

    return render_template('index.html')