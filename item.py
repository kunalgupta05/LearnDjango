import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item {} not found".format(name)}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            name, price = row[0], row[1]
            return {"item": {"name": name, "price": price}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "Item {} already exists".format(name)}, 400  # HTTP status code 400 for bad request

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items values (?, ?)"
        name, price = item['name'], item['price']
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()
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

