# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id       = db.Column(db.Integer,     primary_key=True)
    user     = db.Column(db.String(64),  unique = True)
    nickname = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(500))
    points   = db.Column(db.Integer)

    def __init__(self, user, nickname, password):
        self.user       = user
        self.password   = password
        self.nickname   = nickname
        self.points      = 0

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 
