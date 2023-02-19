from flask import jsonify, request, make_response, Blueprint
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users
import uuid
import jwt
import datetime

auth_blueprint = Blueprint('auth_blueprint', __name__)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            try:
                data = jwt.decode(token, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "HS256")
                current_user = Users.query.filter_by(public_id=data['public_id']).first()
                return f(current_user, *args, **kwargs)
            except Exception as ex:
                return jsonify({'message': 'Something is wrong either an error has occurred or your token is invalid',
                                'more detail': str(ex)})

        if not token:
            return jsonify({'message': 'a valid token is missing'})

    return decorator

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def signup_user():
    """Register user for API via username and password"""
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('verification failed', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
        return jsonify({'token': token})

    return make_response('verification failed', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
