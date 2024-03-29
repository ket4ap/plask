from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    #__name__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    #def __repr__(self):
        #return '<User %r>' % self.username