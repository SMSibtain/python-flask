from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.store import Store, StoreList
from resources.user import Auth, UserRegister
from resources.item import Items, ItemList
from datetime import timedelta
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "smsrn123"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)
db.init_app(app)
# app.secret_key = 'smsrn123'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)  # , authenticate, identity)  # /auth

api.add_resource(Auth, '/auth')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
