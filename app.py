from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import *
from resources.store import *

app = Flask(__name__) # instance of Flask class
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False # with false doesn't keep track of all the modification
app.secret_key = 'bruno' # MUST BE SECRET AND POSSIBLY COMPLEX.
api = Api(app)

jwt = JWT(app, authenticate, identity) # new endpoint /auth

# mapping class to endpoints:
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # make accessible Item resource via api http://localhost:5000/item/name
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db # circular import
    db.init_app(app)
    app.run(port=5000, debug=True) # REMOVE DEBUG MODE IN PROD
