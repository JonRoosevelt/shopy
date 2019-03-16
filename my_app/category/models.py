from my_app import db
from marshmallow import fields, schema


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    item = db.relationship("Item", cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False)
    quantity = db.Column(db.Integer, unique=False)
    checked = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', lazy='subquery',
                               backref='items', cascade='all, delete-orphan',
                               single_parent=True)

    def __init__(self, name, description, quantity, checked, category):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.checked = checked
        self.category = category


class ItemSchema(schema.Schema):
    name = fields.String()
    description = fields.String()
    quantity = fields.String()
    checked = fields.Boolean()
    category = fields.Int()
    id = fields.Int()


class CategorySchema(schema.Schema):
    name = fields.String()
    id = fields.Integer()
    items = fields.Nested(ItemSchema, many=True)


class DataSchema(schema.Schema):
    data = fields.Nested(CategorySchema, many=True)