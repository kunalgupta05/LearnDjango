import sqlite3


class ItemModel(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return dict(name=self.name, price=self.price)

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

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items values (?, ?)"
        name, price = item['name'], item['price']
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        name, price = item['name'], item['price']
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()
