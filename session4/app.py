from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
# app.secret_key = 'smsrn123'
api = Api(app)

jwt = JWTManager(app)  # , authenticate, identity)  # /auth

items = []

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


class Auth(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = authenticate(username, password)
        if user is None:
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=username)
        print(access_token)
        return {'access_token': access_token}


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
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'data': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f'An item with name {name} already exist.'}, 404

        data = Items.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Items.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'data': items}


api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Auth, '/auth')

app.run(port=5000, debug=True)
