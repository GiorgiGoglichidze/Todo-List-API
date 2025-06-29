from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100),unique = True)
    password = db.Column(db.String(100))
    confirm_password = db.Column(db.String(100))

    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)