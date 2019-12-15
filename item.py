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

        try:
            self.insert(item)
        except:
            return {'message': 'An error occurred while inserting the item'}, 500 # HTTP code for internal server error

        return item, 201   # HTTP status code 201 when some object is created

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items values (?, ?)"
        name, price = item['name'], item['price']
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()

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
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occurred while inserting the item'}, \
                       500  # HTTP code for internal server error
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occurred while updating the item'}, \
                       500  # HTTP code for internal server error

        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        name, price = item['name'], item['price']
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()


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

