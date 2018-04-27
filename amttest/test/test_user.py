from flask import Flask
from flask_testing import TestCase

from ..database import db
from ..database.utils import table2dict
from ..database.tables.user import User
from ..errors import *
from ..routes import user

from ..helpers import token
from ..helpers.bphandler import BPHandler

class TestUser(TestCase):

    def create_app(self):
        print('creating app')
        app = Flask('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        BPHandler.register_blueprints(app)
        db.app = app
        db.init_app(app)
        return app


    def setUp(self):
        print('running setup')
        db.create_all()
        self.token = token.gen_token()


    def tearDown(self):
        print('running teardown')
        db.session.remove()
        db.drop_all()


    def test_get_user(self):
        user = User(name='test', fbuserid='abc123', email='test@test.test')
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        response = self.client.get('/amttest/api/users/1')
        self.assertEqual(response.json,
                         table2dict(user),
                         'get_user response json does not match record')
        self.assert200(response, 'success status code not 200')

        response = self.client.get('/amttest/api/users/42')
        self.assert400(response, 'non existent user should return 400')

        user.archive = True
        db.session.commit()
        db.session.refresh(user)

        response = self.client.get('/amttest/api/users/1')
        self.assert400(response, 'archived users should not return')

