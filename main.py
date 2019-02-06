from bs4 import BeautifulSoup
import requests

calendar_url = "https://ugradcalendar.uwaterloo.ca/page/ENG-Computer-Engineering-Electrical-Engineering"

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

class Course:
    name = ''
    code = ''
    program = ''

    def __init__(self, name, code,  program):
        self.name = name
        self.program = program
        self.code = code

def get_site_content(url):
    req = requests.get(url)
    text = req.text.encode('utf-8')

    soup = BeautifulSoup(text, 'html.parser')

    main_content = soup.find('span', {'class':'MainContent'})

    return main_content

def get_course_list(main_content):
    table = main_content.find('table')

    rows = table.find_all('tr')

    return rows

def get_courses_from_list(rows):
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
            
            if not course_name == 'n/a':
                course = Course(course_name, code, program)
                terms[academic_term].append(course)

def get_courses(year):
    url = calendar_url + "/?ActiveDate=9/1/" + year
    
    content = get_site_content(url)
    rows = get_course_list(content)
    get_courses_from_list(rows)

def main():
    year = raw_input("Please select your starting year: ")

    get_courses(year)

    term = raw_input("Please select a term: ")

    for course in terms[term]:
        print course.code

if __name__ == '__main__':
    main()
