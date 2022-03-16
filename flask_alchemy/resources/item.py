from multiprocessing import connection
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel


class Items(Resource):
    parser = reqparse.RequestParser()
    # FILTER REQUIRED PAYLOAD USING PARSING - START
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can not be left black!")
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help="Every ite need a store id")
    # FILTER REQUIRED PAYLOAD USING PARSING - START

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name \'{name}\' already exist.'}, 400

        data = Items.parser.parse_args()

        item = ItemModel(name, **data)  # data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
        # if result.rowcount > 0:
        return {'message': 'Item deleted'}
        # return {'message': 'Item not found'}

    def put(self, name):
        data = Items.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)  # data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
