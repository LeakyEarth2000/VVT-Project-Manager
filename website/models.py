from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    # user model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    usertype = db.Column(db.String(50), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Note(db.Model):
    # note model
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Project(db.Model):
    # project model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    # task model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    progress = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.Date, nullable=True)  # Add this line
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    