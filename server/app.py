#!/usr/bin/env python3

from flask import Flask, request, make_response
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

@app.route('/vendors')
def vendors():
    return make_response([vendor.to_dict() for vendor in Vendor.query.all()], 200)

@app.route('/vendors/<int:id>')
def vendors_by_id(id):
    vendor = Vendor.query.filter_by(id=id).first()

    if not vendor:
        return make_response({'error': 'Vendor not found'}, 404)
    return make_response(vendor.to_dict(), 200)

@app.route('/sweets')
def sweets():
    return make_response([sweet.to_dict() for sweet in Sweet.query.all()], 200)

@app.route('/sweets/<int:id>')
def sweets_by_id(id):
    sweet = Sweet.query.filter_by(id=id).first()

    if not sweet:
        return make_response({'error': 'Sweet not found'}, 404)
    return make_response(sweet.to_dict(), 200)

@app.route('/vendor_sweets', methods = ['POST'])
def vendor_sweets():
    new_vendor_sweet = VendorSweet(
        price = request.get_json()['price'],
        vendor_id = request.get_json()['vendor_id'],
        sweet_id = request.get_json()['sweet_id']
    )
    db.session.add(new_vendor_sweet)
    db.session.commit()

    try:
        return make_response(new_vendor_sweet.to_dict(), 201)
    except ValueError:
        return make_response({'error': 'Validation errors'}, 400)

@app.route('/vendor_sweets/<int:id>', methods = ['DELETE'])
def vendor_sweets_by_id(id):
    vendor_sweet = VendorSweet.query.filter_by(id=id).first()
    if not vendor_sweet:
        return make_response({'error': 'VendorSweet not found'}, 404)
    elif request.method == 'DELETE':
        db.session.delete(vendor_sweet)
        db.session.commit()

        return make_response({}, 204)
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
