from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# api works with resources, and every resource is a class
# resource, what the client interact with

class Item(Resource): # copy of Resource class, with something changed

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )

    #@jwt_required()
    def get(self, name): # implement the get method for this resource
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occured when fetching the item"}, 500 # not request fault, server problem
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    #@jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item named '{}' already exists.".format(name)}, 400 # bad request, item already exists

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"}, 500 # not request fault, server problem

        return item.json(), 201

    #@jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "The item has been deleted."}
        return {"message": "No item named {} has been found".format(name)}, 404

    #@jwt_required()
    def put(self, name): # can be used to modifiy existing item, or to create a new one
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": "An error occour inserting the item"}, 500
        else:
            try:
                item.price = data["price"] # values in item will change according to data
                item.store_id = data['store_id']
            except:
                return {"message": "An error occour updating the item"}, 500

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    #@jwt_required()
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
