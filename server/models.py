from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    def __repr__(self):
        return f'Name: {self.name}'
    
    vendor_sweets = db.relationship('VendorSweet', backref='sweet')
    vendors = association_proxy('vendor_sweets', 'vendor')

    serialize_rules = ('-created_at', '-updated_at', '-vendor_sweets', '-vendors')

class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))

    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError('Validation errors')
        return price

    def __repr__(self):
        return f'Price: {self.price} | vendor_id: {self.vendor_id}| sweet_id: {self.sweet_id}'

    serialize_rules = ('-created_at', '-updated_at', '-vendor_id', '-sweet_id')

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    vendor_sweets = db.relationship('VendorSweet', backref='vendor')
    sweets = association_proxy('vendor_sweets', 'sweet')

    def __repr__(self):
        return f'Name: {self.name}'
    
    serialize_rules = ('-created_at', '-updated_at', '-vendor_sweets', '-sweets')