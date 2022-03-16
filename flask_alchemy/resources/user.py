from multiprocessing import connection
import sqlite3
from flask_restful import Resource, request, reqparse
from flask_jwt_extended import create_access_token
from models.user import UserModel

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


class Auth(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = UserModel.find_by_username(username)
        # user = authenticate(username, password)
        if user is not None and user.password == password:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token, "msg": "Log in successful"}
        return {"msg": "Bad username or password"}, 401


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field can not be black')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field can not be black')

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user is not None:
            return {'message': 'Username already exist'}, 422

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'Username created successfully.'}, 201
