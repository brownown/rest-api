from app import app
from db import db

db.init_app(app)

@app.before_first_request # this decorator will start before the first request
def create_tables():
    db.create_all()
