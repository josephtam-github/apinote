from app import db, ma
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    notes = db.relationship('Notes', back_populates='created_by', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    # A full type-written page usually contains 2kb of character hence 2048 char limit
    created_on = db.Column(db.DateTime, default=datetime.now())
    created_by = db.relationship('Users', back_populates='notes')

    def __repr__(self):
        return f'User {self.username}'

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')
        model = Note


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
