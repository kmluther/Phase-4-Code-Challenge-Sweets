#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate

from models import db, Sweet, Vendor, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
