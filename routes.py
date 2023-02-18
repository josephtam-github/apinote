from flask import jsonify, Blueprint
from auth import token_required

route_blueprint = Blueprint('route_blueprint', __name__)


@route_blueprint.route('/')
def hello_world():  # put application's code here\
    """Welcomes client and redirects to API documentation"""
    return jsonify({'message': 'Welcome to apinote'})
