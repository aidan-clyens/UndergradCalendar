from flask import g
import sqlite3

DATABASE = 'app/courses.db'

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
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=()):
    cur = get_db().execute(query, args)
    res = cur.fetchall()
    cur.close()

    get_db().commit()

    return res
