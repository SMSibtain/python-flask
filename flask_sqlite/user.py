from multiprocessing import connection
import sqlite3

from flask_restful import Resource, request, reqparse
from flask_jwt_extended import create_access_token


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(self, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = self(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(self, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = self(*row)
        else:
            user = None

        connection.close()
        return user


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
class Auth(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = User.find_by_username(username)
        # user = authenticate(username, password)
        if user is not None and user.password == password:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}
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

        user = User.find_by_username(data['username'])
        if user is not None:
            return {'message': 'Username already exist'}, 422

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'Username created successfully.'}, 201
