from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from datetime import datetime

uwflow_url = "https://uwflow.com/"
calendar_url = "https://ugradcalendar.uwaterloo.ca/"
ece_page = "page/ENG-Computer-Engineering-Electrical-Engineering"

min_year = 2012
max_year = datetime.now().year

class Course:
    year = 0
    term = ''
    name = ''
    code = ''
    program = ''
    cls = 0
    tut = 0
    lab = 0
    url = ''
    uwflow_url = ''

    def __init__(self, name, code):
        self.name = name
        self.code = code

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        year = request.form['year']

        terms = get_courses(year)

        if int(year) >= min_year and int(year) <= max_year:
            return render_template('courses.html', terms=terms)

    return render_template('index.html')

def get_site_content(url):
    req = requests.get(url)
    text = req.text.encode('utf-8')

    soup = BeautifulSoup(text, 'html.parser')

    return soup

def get_course_list(soup):
    main_content = soup.find('span', {'class':'MainContent'})
    table = main_content.find('table')

    rows = table.find_all('tr')

    return rows

def get_courses_from_list(rows):
    terms = {
        '1A' : [],
        '1B' : [],
        '2A' : [],
        '2B' : [],
        '3A' : [],
        '3B' : [],
        '4A' : [],
        '4B' : []
    }

    for [i, row] in enumerate(rows):
        cols = row.find_all('td')

        if len(cols) > 3:
            if 'Academic Term' in row.text:
                course_name = cols[3].text.strip()
                code = cols[2].text.strip()
                program = cols[1].text.strip()
                academic_term = cols[0].text.strip()[14:16]
                
                if len(cols) > 6:
                    cls = float(cols[4].text.strip())
                    tut = float(cols[5].text.strip())
                    lab = float(cols[6].text.strip())
            else:
                course_name = cols[2].text.strip()
                code = cols[1].text.strip()
                program = cols[0].text.strip()

                if len(cols) > 5:
                    cls = float(cols[3].text.strip())
                    tut = float(cols[4].text.strip())
                    lab = float(cols[5].text.strip())

            if not 'COOP' in course_name:
                index = course_name.find('(')
                if index > -1:
                    course_name = course_name[:index]

                if program == 'n/a':
                    program = 'both'

                course = Course(course_name, code)
                course.year = year
                course.term = academic_term
                course.program = program
                course.cls = cls
                course.tut = tut
                course.lab = lab
                terms[academic_term].append(course)

    return terms

def add_course_urls(year, terms):
    course_list_url = "http://www.ucalendar.uwaterloo.ca/" + (year[2:5] + str((int(year[2:5]) + 1))) + "/COURSE/course-ECE.html"

    for term in terms.values():
        for course in term:
            course.url = course_list_url + "#" + course.code.replace(' ', '')
            course.uwflow_url = uwflow_url + "course/" + course.code.replace(' ', '').lower()

def get_courses(year):
    url = calendar_url + ece_page + "/?ActiveDate=9/1/" + year
    
    content = get_site_content(url)
    rows = get_course_list(content)
    terms = get_courses_from_list(year, rows)

    add_course_urls(year, terms)

    return terms

if __name__ == '__main__':
    app.run()
