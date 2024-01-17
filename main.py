from flask import Flask

import models
from models import db

import sys


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

if sys.argv[1] == "create-database":
    with app.app_context():
        db.create_all()
    exit(0)

if __name__ == "__main__":
    app.run()
