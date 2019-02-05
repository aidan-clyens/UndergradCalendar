from bs4 import BeautifulSoup
import requests

url = "https://ugradcalendar.uwaterloo.ca/page/ENG-Computer-Engineering-Electrical-Engineering/?ActiveDate=9/1/2016"

class Course:
    name = ''
    code = ''
    program = ''

    def __init__(self, name, code,  program):
        self.name = name
        self.program = program
        self.code = code

class Term:
    name = ''
    courses = []

    def __init__(self, name):
        self.name = name

    def add_course(self, course):
        self.courses.append(course)

terms = {
    '1A' : Term('1A'),
    '1B' : Term('1B'),
    '2A' : Term('2A'),
    '2B' : Term('2B'),
    '3A' : Term('3A'),
    '3B' : Term('3B'),
    '4A' : Term('4A'),
    '4B' : Term('4B')
}

req = requests.get(url)
text = req.text.encode('utf-8')

soup = BeautifulSoup(text, 'html.parser')

main_content = soup.find('span', {'class':'MainContent'})
table = main_content.find('table')

rows = table.find_all('tr')

for [i, row] in enumerate(rows):
    cols = row.find_all('td')

    if len(cols) > 3:
        if 'Academic Term' in row.text:
            course_name = cols[3].text.strip()
            code = cols[2].text.strip()
            program = cols[1].text.strip()
            academic_term = cols[0].text.strip()[14:16]
        else:
            course_name = cols[2].text.strip()
            code = cols[1].text.strip()
            program = cols[0].text.strip()

        print academic_term
        course = Course(course_name, code, program)
        terms[academic_term].add_course(course)

#for term in terms.values():
    #print term.name

    #for course in term.courses:
        #print course.code, course.name
