from app import app
from flask import request, render_template
from . import webscraper
from datetime import datetime
import os

year = "2016"

@app.route('/')
def index():
    ws = webscraper.WebScraper()
    terms = ws.get_courses(year)

    return render_template('courses.html', terms=terms)