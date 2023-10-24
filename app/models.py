from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import enum

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    super_name = db.Column(db.String(20))

    # Establish a one-to-many relationship from Hero to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='hero')

class Power(db.Model,SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(20))

    # Establish a one-to-many relationship from Power to HeroPower
    power_heroes = db.relationship('HeroPower', back_populates='power')

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropowers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    

    # Establish many-to-one relationships to Hero and Power
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='power_heroes')

# add any models you may need. 