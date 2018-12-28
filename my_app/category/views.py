from flask import request, jsonify
from my_app import db, app
from my_app.category.models import (
    Category, category_schema, categories_schema,
    Item, item_schema, items_schema,
)


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


# endpoint to create new item
@app.route("/category/<id>/item", methods=["POST"])
def add_item(id):
    name = request.json['name']
    description = request.json['description']
    quantity = request.json['quantity']

    new_item = Item(name, description, quantity)

    db.session.add(new_item)
    db.session.commit()

    return jsonify(request.json)


# endpoint to show all items inside a category
@app.route("/category/<category_id>/item", methods=["GET"])
def get_itens():
    all_items = Category.Item.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result)


# endpoint to get the item detail by id
@app.route("category/<category_id>/item/<id>", methods=["GET"])
def item_detail(id):
    item = Category.Item.query.get(id)
    return item_schema.jsonify(item)


# endpoint to update item
@app.route("category<category_id>/item/<id>", methods=["PUT"])
def item_update(id):
    item = Category.Item.query.get(id)
    name = request.json['name']
    description = request.json['description']
    quantity = request.json['quantity']

    item.name = name
    item.description = description
    item.quantity = quantity

    db.session.commit()
    return item_schema.jsonify(item)


# endpoint to delete item
@app.route("/category<category_id>/item/<id>", methods=["DELETE"])
def item_delete(id):
    item = Category.Item.query.get(id)
    db.session.delete(item)
    db.session.commit()

    return item_schema.jsonify(item)
