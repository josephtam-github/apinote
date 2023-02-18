from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from auth import auth_blueprint
from routes import route_blueprint
from os import urandom


app = Flask(__name__)
app.register_blueprint(auth_blueprint)
app.register_blueprint(route_blueprint)
app.app_context().push()
app.config['SECRET_KEY'] = urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apinote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)

if __name__ == '__main__':
    app.run()
