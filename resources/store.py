from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store {} not found".format(name)}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store {} already exists".format(name)}, 400  # HTTP status code 400 for bad request

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while inserting the store in database'}, 500  # HTTP code for ISE

        return store.json(), 201   # HTTP status code 201 when some object is created

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

