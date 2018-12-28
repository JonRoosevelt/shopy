from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

    def __init__(self, name):
        self.name = name


class CategorySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name',)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False)
    quantity = db.Column(db.Integer, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)

    def __init__(self, name, description, quantity):
        self.name = name
        self.description = description
        self.quantity = quantity


class ItemSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'description', 'quantity')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


# endpoint to create new category
@app.route("/category", methods=["POST"])
def add_category():
    name = request.json['name']

    new_category = Category(name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(request.json)


# endpoint to show all categories
@app.route("/category", methods=["GET"])
def get_category():
    all_categories = Category.query.all()
    result = categories_schema.dump(all_categories)
    return jsonify(result)


# endpoint to get the cateogory detail by id
@app.route("/category/<id>", methods=["GET"])
def category_detail(id):
    category = Category.query.get(id)
    return category_schema.jsonify(category)


# endpoint to update category
@app.route("/category/<id>", methods=["PUT"])
def category_update(id):
    category = Category.query.get(id)
    name = request.json['name']

    category.name = name

    db.session.commit()
    return category_schema.jsonify(category)


# endpoint to delete category
@app.route("/category/<id>", methods=["DELETE"])
def category_delete(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()

    return category_schema.jsonify(category)


if __name__ == '__main__':
    app.run(debug=True)
