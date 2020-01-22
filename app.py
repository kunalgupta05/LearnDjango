import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, Items
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = False
app.secret_key = "jose"
api = Api(app)

db.init_app(app)

# To create the data.db file using sqlalchemy
@app.before_first_request
def create_tables():
    db.create_all()


# Doesn't create the auth endpoint in the background. Has to be created manually.
jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
