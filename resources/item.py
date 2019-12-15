import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {"message": "Item {} not found".format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item {} already exists".format(name)}, 400  # HTTP status code 400 for bad request

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            ItemModel.insert(item)
        except:
            return {'message': 'An error occurred while inserting the item'}, 500 # HTTP code for internal server error

        return item, 201   # HTTP status code 201 when some object is created

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items where name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                ItemModel.insert(updated_item)
            except:
                return {'message': 'An error occurred while inserting the item'}, \
                       500  # HTTP code for internal server error
        else:
            try:
                ItemModel.update(updated_item)
            except:
                return {'message': 'An error occurred while updating the item'}, \
                       500  # HTTP code for internal server error

        return updated_item


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = [dict(name=row[0], price=row[1]) for row in result]
        connection.commit()
        connection.close()
        return {'items': items}

