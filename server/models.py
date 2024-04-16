from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def get_uuid(length=16):
    return uuid4().hex

# Define the models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date_id = db.Column(db.Integer, db.ForeignKey('due_date.id'))
    due_date = db.relationship('DueDate', backref='task', uselist=False)
    subtasks = db.relationship('Subtask', backref='task', lazy=True)
    assignees = db.relationship('User', secondary='task_assignees', backref='tasks', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.serialize() if self.due_date else None,
            'subtasks': [subtask.serialize() for subtask in self.subtasks]
        }

class DueDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.Date, nullable=False)

    def serialize(self):
        return {'id': self.id, 'due_date': self.due_date}

class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def serialize(self):
        return {'id': self.id, 'title': self.title}

task_assignees = db.Table('task_assignees',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(64))
    public_id = db.Column(db.String(36), unique=True, nullable=False, default=str(uuid4()))

    def serialize(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'public_id': self.public_id}

    @property
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
