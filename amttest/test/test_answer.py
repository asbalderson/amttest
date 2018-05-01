import json

from flask import Flask
from flask_testing import TestCase

from ..database import db
from ..database.utils import table2dict
from ..database.tables.answer import Answer
from ..errors import *
from ..routes import answer

from ..helpers import token
from ..helpers.bphandler import BPHandler

class TestAnswer(TestCase):

    def create_app(self):
        app = Flask('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        BPHandler.register_blueprints(app)
        db.app = app
        db.init_app(app)
        return app


    def setUp(self):
        db.create_all()
        this_token = token.gen_token()
        self.header_dict = {'token': this_token}


    def tearDown(self):
        db.session.remove()
        db.drop_all()