from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from os import urandom


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apinote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)

from auth import auth_blueprint
from routes import route_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(route_blueprint)

if __name__ == '__main__':
    app.run()
