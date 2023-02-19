from flask import jsonify, Blueprint, request
from sqlalchemy import exc
from auth import token_required
from flask_restful import Resource
from models import Notes, note_schema, notes_schema, db
from app import api

route_blueprint = Blueprint('route_blueprint', __name__)


@route_blueprint.route('/', methods=['GET', 'POST'])
def hello_world():
    """Welcomes client and redirects to API documentation"""
    return jsonify({'message': 'Welcome to apinote'})


class NoteCreate(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        new_post = Notes(
            title=request.json['title'],
            content=request.json['content'],
            user_id=current_user.id
        )
        try:
            db.session.add(new_post)
            db.session.commit()
        except exc.SQLAlchemyError:
            return 'sqlerror'
        return note_schema.dump(new_post)


api.add_resource(NoteCreate, '/create')