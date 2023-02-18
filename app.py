from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import urandom


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


if __name__ == '__main__':
    app.run(DEBUG=True)
