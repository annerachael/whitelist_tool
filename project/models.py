from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class WhitelistedMSISDN(UserMixin, db.Model):
    __tablename__ = 'whitelisted_msisdn'
    id = db.Column(db.Integer, primary_key=True)
    msisdn = db.Column(db.Integer, unique=True, nullable=False)
    service_line = db.Column(db.String(10), nullable=False)