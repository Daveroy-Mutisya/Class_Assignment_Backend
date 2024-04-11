from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()

def get_uuid(length=16):
    return uuid4().hex

# Define the models
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date_id = db.Column(db.Integer, db.ForeignKey('due_date.id'))
    subtasks = db.relationship('Subtask', backref='task', lazy=True)
    assignees = db.relationship('User', secondary='task_assignees', backref='tasks', lazy='dynamic')

class DueDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.Date, nullable=False)
    task = db.relationship('Tasks', backref='due_date', uselist=False)

class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

task_assignees = db.Table('task_assignees',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(64))  


