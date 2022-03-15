from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from user import User, Auth, UserRegister
from item import Items, ItemList

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "smsrn123"  # Change this!
# app.secret_key = 'smsrn123'
api = Api(app)

jwt = JWTManager(app)  # , authenticate, identity)  # /auth

api.add_resource(Auth, '/auth')
api.add_resource(UserRegister, '/register')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
