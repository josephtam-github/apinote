from flask import Flask
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from werkzeug.security import generate_password_hash, check_password_hash
from modules import Users
import uuid


app = Flask(__name__)
app.app_context().push()
secret_key = urandom(32)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apinote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here\
    """Welcomes client and redirects to API documentation"""
    return jsonify({'message': 'Welcome to apinote'})


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    """Register user for API via username and password"""
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


if __name__ == '__main__':
    app.run(DEBUG=True)
