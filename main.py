from bs4 import BeautifulSoup
import requests

uwflow_url = "https://uwflow.com/"
calendar_url = "https://ugradcalendar.uwaterloo.ca/"
ece_page = "page/ENG-Computer-Engineering-Electrical-Engineering"

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
    cls = 0
    tut = 0
    lab = 0
    url = ''
    uwflow_url = ''

    def __init__(self, name, code):
        self.name = name
        self.code = code

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
    
            course = Course(course_name, code)
            course.program = program
            course.cls = cls
            course.tut = tut
            course.lab = lab
            terms[academic_term].append(course)

def add_course_urls(year):
    course_list_url = "http://www.ucalendar.uwaterloo.ca/" + (year[2:5] + str((int(year[2:5]) + 1))) + "/COURSE/course-ECE.html"

    for term in terms.values():
        for course in term:
            course.url = course_list_url + "#" + course.code.replace(' ', '')
            course.uwflow_url = uwflow_url + "course/" + course.code.replace(' ', '').lower()

def get_courses(year):
    url = calendar_url + ece_page + "/?ActiveDate=9/1/" + year
    
    content = get_site_content(url)
    rows = get_course_list(content)
    get_courses_from_list(rows)

    add_course_urls(year)

    return url

def main():
    year = raw_input("Please select your starting year: ")

    url = get_courses(year)

    print "Showing ECE calendar from", year
    print url, "\n"

    term = raw_input("Please select a term: ")
    
    if term in terms.keys():
        for course in terms[term]:
            print course.code, "  ", course.url, "  ",  course.uwflow_url, "  ", course.cls, "  ", course.tut, "  ", course.lab
    else:
        print "Invalid key:", term

if __name__ == '__main__':
    main()
