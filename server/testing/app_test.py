import json
from os import environ
from flask import request

from app import app
from models import db, Sweet, Vendor, VendorSweet

class TestApp:
    '''Flask application in app.py'''

    def test_gets_sweets(self):
        '''retrieves sweets with GET requests to /sweets.'''

        with app.app_context():
            ccc = Sweet(name="Chocolate Chip Cookie")
            db.session.add(ccc)
            db.session.commit()

            response = app.test_client().get('/sweets').json
            sweets = Sweet.query.all()
            assert [sweet['id'] for sweet in response] == [sweet.id for sweet in sweets]
            assert [sweet['name'] for sweet in response] == [sweet.name for sweet in sweets]

    def test_gets_sweet_by_id(self):
        '''retrieves one sweet using its ID with GET request to /sweets/<int:id>.'''

        with app.app_context():
            ccc = Sweet(name="Chocolate Chunk Cookie")
            db.session.add(ccc)
            db.session.commit()

            response = app.test_client().get(f'/sweets/{ccc.id}').json
            assert response['name'] == ccc.name

    def test_gets_vendors(self):
        '''retrieves vendors with GET requests to /vendors.'''

        with app.app_context():
            insomnia_cookies = Vendor(name="Insomnia Cookies")

            db.session.add(insomnia_cookies)
            db.session.commit()

            response = app.test_client().get('/vendors').json
            vendors = Vendor.query.all()
            assert [vendor['id'] for vendor in response] == [vendor.id for vendor in vendors]
            assert [vendor['name'] for vendor in response] == [vendor.name for vendor in vendors]

    def test_gets_vendor_by_id(self):
        '''retrieves one vendor using its ID with GET request to /vendors/<int:id>.'''

        with app.app_context():
            cookies_cream = Vendor(name="Cookies Cream")
            db.session.add(cookies_cream)
            db.session.commit()

            response = app.test_client().get(f'/vendors/{cookies_cream.id}').json
            assert response['name'] == cookies_cream.name

    def test_delete_vendor_by_id(self):
        '''updates one vendor using its ID and JSON input for its fields with a delete request to /vendors/<int:id>.'''

        with app.app_context():
            sweet = Sweet(name="Duane Park Patisserie")
            vendor = Vendor(name="Tribeca Treats")
            vendor_sweet = VendorSweet(price = 100, sweet = sweet, vendor = vendor)
            db.session.add(vendor)
            db.session.commit()

            app.test_client().delete(
                f'/vendor_sweets/{vendor_sweet.id}').json

            vendor_sweet = VendorSweet.query.filter(VendorSweet.id == vendor_sweet.id).one_or_none()

            assert not vendor_sweet

    def test_creates_sweet_vendor(self):
        '''creates one sweet_vendor using, price, sweet_id, and a vendor_id with a POST request to /sweet_vendors.'''

        with app.app_context():

            sweet = Sweet(name="Duane Park Patisserie")
            vendor = Vendor(name="Tribeca Treats")

            db.session.add(sweet)
            db.session.add(vendor)
            db.session.commit()

            response = app.test_client().post(
                'vendor_sweets',
                json={
                    'price': 5,
                    'sweet_id': sweet.id,
                    'vendor_id': vendor.id,
                }
            ).json
            print(response)
            assert response['sweet']['name'] == sweet.name
            assert response['price'] == 5
            assert response['sweet']['id'] == sweet.id
            assert response['vendor']['id'] == vendor.id
            assert sweet.vendor_sweets[0].price == 5
            assert sweet.vendor_sweets[0].sweet_id == sweet.id
            assert sweet.vendor_sweets[0].vendor_id == vendor.id

    def test_validates_sweet_vendor_price(self):
        '''returns an error message if a POST request to /sweet_vendors contains a non negetive "price" value.'''

        with app.app_context():

            sweet = Sweet(name="Duane Park Patisserie")
            vendor = Vendor(name="Tribeca Treats")
            db.session.add_all([sweet, vendor])
            db.session.commit()

            response = app.test_client().post(
                'vendor_sweets',
                json={
                    'price': -1,
                    'sweet_id': sweet.id,
                    'vendor_id': vendor.id,
                }
            ).json

            assert response['error'] == "Validation errors"
