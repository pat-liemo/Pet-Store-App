from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(450), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    
    # Relationships
    pets = db.relationship('Pet', back_populates='user', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)
    
    
    #validate the users email to have an @
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address. Must contain '@'.")
        return email


    #validate the phone number to have 10 digits
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not (isinstance(phone_number, int) and len(str(phone_number)) == 10):
            raise ValueError("Invalid phone number. Must be a numeric value with 10 digits.")
        return phone_number
    
class Pet(db.Model):
    
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    species = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_store_id = db.Column(db.Integer, db.ForeignKey('pet_stores.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Relationships
    user = db.relationship('User', back_populates='pets', lazy=True)
    pet_store = db.relationship('PetStore', back_populates='pets', lazy=True)

class Review(db.Model):
    
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    Rating = db.Column(db.Float, nullable=False)
    Comments = db.Column(db.String, nullable=False)
    pet_store_id = db.Column(db.Integer, db.ForeignKey('pet_stores.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Relationships
    pet_store = db.relationship('PetStore', back_populates='reviews', lazy=True)
    user = db.relationship('User', back_populates='reviews', lazy=True)

class PetStore(db.Model):
    
    __tablename__ = 'pet_stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    
    
    # Relationships
    reviews = db.relationship('Review', back_populates='pet_store', lazy=True)
    pets = db.relationship('Pet', back_populates='pet_store', lazy=True)
