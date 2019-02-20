from flask import g
import sqlite3

DATABASE = 'app/courses.db'

def init_db():
    db = get_db()
    with open('app/schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

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

    return res
