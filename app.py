from flask import Flask
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import urandom


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apinote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    return jsonify({'message': 'apinote'})


if __name__ == '__main__':
    app.run(DEBUG=True)
