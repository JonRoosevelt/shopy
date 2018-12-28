from my_app import db, ma


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
