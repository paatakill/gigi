from ext import db, login_manager
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import datetime

time = datetime.datetime.now()

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class Reviewmodel(db.Model):

    __tablename__ = "reviewmodel"

    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(120), nullable=True) 


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=time)

    review_id = db.Column(db.Integer, nullable=False)


class User(db.Model, BaseModel, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    phonenum = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    role = db.Column(db.String(), nullable=False)

    def __init__(self,username, password, phonenum, date, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.phonenum = phonenum
        self.date = date
        self.role = role
        


@login_manager.user_loader   
def load_user(user_id):
    return User.query.get(user_id)

class Email(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False)

