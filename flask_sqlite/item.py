from multiprocessing import connection
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required


class Items(Resource):
    parser = reqparse.RequestParser()
    # FILTER REQUIRED PAYLOAD USING PARSING - START
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can not be left black!")
    # FILTER REQUIRED PAYLOAD USING PARSING - START

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row is not None:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': f'An item with name \'{name}\' already exist.'}, 400

        data = Items.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {"message": "An error occured inserting the item."}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        result = cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        if result.rowcount > 0:
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}

    def put(self, name):
        data = Items.parser.parse_args()

        item = self.find_by_name(name)
        updatedItem = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updatedItem)
                return updatedItem, 201
            except:
                return {"message": "An error occured inserting the item."}, 500
        else:
            try:
                self.update(updatedItem)
                return updatedItem, 200
            except:
                return {"message": "An error while updating the item."}, 500


class ItemList(Resource):
    def get(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'data': items}
