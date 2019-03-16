from flask import request, jsonify, Blueprint
from my_app import db
from my_app.category.models import (
    Category, CategorySchema,
    Item, ItemSchema
)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


shopy = Blueprint('shopy', __name__)


# Test
@shopy.route("/")
def hello_world():
    return "Hello World"


# endpoint to create new category
@shopy.route("/category", methods=["POST"])
def add_category():
    name = request.json['name']

    new_category = Category(name)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(request.json)


# endpoint to show all categories
@shopy.route("/category", methods=["GET"])
def get_category():
    all_categories = Category.query.all()
    result = CategorySchema().dump(all_categories, many=True)
    return jsonify({'categories': result})


# endpoint to get the cateogory detail by id
@shopy.route("/category/<int:id>", methods=["GET"])
def category_detail(id):
    category = Category.query.get(id)
    result = CategorySchema().dump(category, many=False)
    return jsonify({'category': result})


# endpoint to update category
@shopy.route("/category/<int:id>", methods=["PUT"])
def category_update(id):
    category = Category.query.get(id)
    name = request.json['name']
    category.name = name
    db.session.commit()
    result = CategorySchema().dump(category, many=False)
    return jsonify({'category': result})


# endpoint to delete category
@shopy.route("/category/<int:id>", methods=["DELETE"])
def category_delete(id):
    category = Category.query.get(id)
    result = CategorySchema().dump(category, many=False)
    db.session.delete(category)
    db.session.commit()

    return jsonify(result)


# endpoint to create new item
@shopy.route("/category/<int:category_id>/item", methods=["POST"])
def add_item(category_id):
    name = request.json['name']
    description = request.json['description']
    quantity = request.json['quantity']
    checked = request.json['checked']
    category_id = Category.query.get(category_id)

    new_item = Item(name, description, quantity, checked, category_id)

    db.session.add(new_item)
    db.session.commit()

    return jsonify(request.json)


# endpoint to get the item detail by id
@shopy.route("/item/<int:id>", methods=["GET"])
def item_detail(id):
    item = Item.query.get(id)
    result = ItemSchema().dump(item, many=False)
    return jsonify(result)


# endpoint to update item
@shopy.route("/item/<int:id>", methods=["PUT"])
def item_update(id):
    item = Item.query.get(id)
    name = request.json['name']
    description = request.json['description']
    quantity = request.json['quantity']
    checked = request.json['checked']
    category_id = request.json['category_id']

    item.name = name
    item.description = description
    item.quantity = quantity
    item.checked = checked
    item.category_id = category_id

    db.session.commit()
    return jsonify({'name': name,
                    'description': description,
                    'quantity': quantity,
                    'checked': checked,
                    'category_id': category_id})


# endpoint to delete item
@shopy.route("/item/<int:id>", methods=["DELETE"])
def item_delete(id):
    item = Item.query.get(id)
    result = ItemSchema().dump(item)
    db.session.delete(item)
    db.session.commit()

    return jsonify(result)
