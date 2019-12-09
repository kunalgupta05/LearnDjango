import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            name, price = row[0], row[1]
            return {"item": {"name": name, "price": price}}
        return {"message": "Item {} not found".format(name)}, 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "Item {} already exists".format(name)}, 400  # HTTP status code 400 for bad request

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201   # HTTP status code 201 when some object is created

    def delete(self, name):
        # to make sure the below statement does not throw any error as the items variable is defined as well as used
        # in the same sentence
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class Items(Resource):
    def get(self):
        return {'items': items}

