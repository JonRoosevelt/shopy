from flask import jsonify
from my_app import db
from marshmallow_sqlalchemy import ModelSchema


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)

    def __init__(self, name):
        self.name = name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False)
    quantity = db.Column(db.Integer, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='items')

    def __init__(self, name, description, quantity, category):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.category = category


class CategorySchema(ModelSchema):
    class Meta:
        model = Category


class ItemSchema(ModelSchema):
    class Meta:
        model = Item
