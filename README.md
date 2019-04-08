# ECE Undergrad Calendar
Displays the course list from the [University of Waterloo Electrical and Computer Engineering Undergraduate calendar](https://ugradcalendar.uwaterloo.ca/page/ENG-Computer-Engineering-Electrical-Engineering/) in a nicer, more readable format. I always thought it was annoying to navigate this site to look at my course calendar, especially having to go select an archived calendar so I could get to the correct year.

## Getting Started
### Usage
1. Go to https://ece-calendar.herokuapp.com/
2. Select a year from the list
3. You may also select light or dark theme from the front page

### Set Up Virtual Environment
1. Install virtualenv with `sudo apt install virtualenv`
2. Create venv folder in project directory using Python 3.6 with `virtualenv -p /usr/bin/python3.6 venv`
3. Activate using `source venv/bin/activate`
4. Install requirements with `pip install -r requirements.txt`

### Running Development Server
1. Run using Gunicorn with `gunicorn ece-calendar:app`
2. Open on `localhost:8000`
