from flask import jsonify, Blueprint, request, render_template
from sqlalchemy import exc
from auth import token_required
from flask_restful import Resource
from models import Notes, note_schema, notes_schema, db
from app import api

route_blueprint = Blueprint('route_blueprint', __name__)


@route_blueprint.route('/help')
def show_doc():
    """API documentation page"""
    return render_template('index.html')


@route_blueprint.route('/', methods=['GET', 'POST'])
def hello_world():
    """Welcomes client and redirects to API documentation"""
    return jsonify({'message': 'Welcome to apinote!',
                    'documentation': 'https://github.com/josephtam-github/apinote/blob/main/README.md'})


class NoteCreate(Resource):
    """Resource for note creation endpoints"""
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
            return 'internal server error. Please try again later'
        return note_schema.dump(new_post)


api.add_resource(NoteCreate, '/create')


class NoteResource(Resource):
    """Resource for note read, update and delete endpoints"""
    method_decorators = [token_required]

    def get(self, current_user, note_id):
        note = Notes.query.filter_by(note_id=note_id, user_id=current_user.id).first()
        return note_schema.dump(note)

    def post(self, current_user, note_id):
        note = Notes.query.filter_by(note_id=note_id, user_id=current_user.id).first()
        return note_schema.dump(note)

    def patch(self, current_user, note_id):
        note = Notes.query.filter_by(note_id=note_id, user_id=current_user.id).first()
        if note:
            note.title = request.json['title']
            note.content = request.json['content']
            db.session.commit()
            return note_schema.dump(note)
        else:
            return 'requested note does not exist'

    def delete(self, current_user, note_id):
        note = Notes.query.filter_by(note_id=note_id, user_id=current_user.id).first()
        if note:
            db.session.delete(note)
            db.session.commit()
            return 'note successfully deleted'
        else:
            return 'requested note does not exist'


api.add_resource(NoteResource, '/note', '/note/<int:note_id>')


class NoteListResource(Resource):
    """Resource for note listing endpoints"""
    method_decorators = [token_required]

    def get(self, current_user):
        notes = Notes.query.filter_by(user_id=current_user.id).all()
        if notes:
            notelist = []
            for note in notes:
                note_data = {'note_id': note.note_id, 'note_title': note.title, 'note_created': note.created_on}
                notelist.append(note_data)
            return jsonify({'list_of_notes': notelist})
        else:
            return 'no notes available'
        
    def post(self, current_user):
        notes = Notes.query.filter_by(user_id=current_user.id).all()
        if notes:
            notelist = []
            for note in notes:
                note_data = {'note_id': note.note_id, 'note_title': note.title, 'note_created': note.created_on}
                notelist.append(note_data)
            return jsonify({'list_of_notes': notelist})
        else:
            return 'no notes available'    


api.add_resource(NoteListResource, '/list')
