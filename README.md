# ECE Undergrad Calendar
## Getting Started
### Set Up Virtual Environment
1. Install virtualenv with `sudo apt install virtualenv`
2. Create venv folder in project directory using Python 3.6 with `virtualenv -p /usr/bin/python3.6 venv`
3. Activate using `source venv/bin/activate`
4. Install requirements with `pip install -r requirements.txt`

### Running Development Server
1. Run using Gunicorn with `gunicorn ece-calendar:app`
2. Open on `localhost:8000`
