from flask import current_app, g
from . import webscraper as ws
import sqlite3

def init_app(app):
    app.teardown_appcontext(close_db)

def init_db():
    create_table_sql = """CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        start_year INTEGER,
        term TEXT,
        code TEXT,
        name TEXT,
        program TEXT,
        url TEXT
        )
        """

    res = query_db(create_table_sql)

    return res

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=()):
    cur = get_db().execute(query, args)
    res = cur.fetchall()
    cur.close()

    get_db().commit()
    return res

def get_courses_from_db(year):
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

    select_term_sql = """SELECT * FROM courses WHERE start_year='%s' AND term=""" % str(year)

    for t in terms.keys():
        query = select_term_sql + "'" + t + "'"

        res = query_db(query)
        for r in res:
            course = ws.Course()
            course.start_year = year
            course.term = t
            course.code = r[3]
            course.name = r[4]
            course.program = r[5]
            course.url = r[6]
            
            terms[t].append(course)

    return terms
