from flask import Flask

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_mapping(
    DATABASE='app/courses.db'
)

from app import routes
from app import db

db.init_app(app)
