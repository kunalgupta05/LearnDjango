import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store id cannot be empty")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item {} not found".format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item {} already exists".format(name)}, 400  # HTTP status code 400 for bad request

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while inserting the item'}, 500  # HTTP code for internal server error

        return item.json(), 201   # HTTP status code 201 when some object is created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price, item.store_id = data['price'], data['store_id']

        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

