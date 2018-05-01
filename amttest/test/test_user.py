import json

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
        this_token = token.gen_token()
        self.header_dict = {'token': this_token}

    def tearDown(self):
        print('running teardown')
        db.session.remove()
        db.drop_all()


    def test_get_user(self):
        user = User(name='test', fbuserid='abc123', email='test@test.test')
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        response = self.client.get('/amttest/api/user/1')
        self.assert200(response, 'success status code not 200')

        record = table2dict(user)
        self.compare_user(response.json, record)

        response = self.client.get('/amttest/api/user/42')
        self.assert400(response, 'non existent user should return 400')

        user.archive = True
        db.session.commit()
        db.session.refresh(user)

        response = self.client.get('/amttest/api/user/1')
        self.assert400(response, 'archived users should not return')


    def test_get_all_users(self):
        response_empty = self.client.get('amttest/api/user')
        self.assert200(response_empty, 'even an emptry respones sould return values')
        self.assertListEqual(response_empty.json, [])
        user1 = User(name='test1', fbuserid='test123', email='test1@test1.test1')
        db.session.add(user1)
        user2 = User(name='test2', fbuserid='testabc', email='test2@test2.test2')
        db.session.add(user2)
        db.session.commit()
        db.session.refresh(user1)
        db.session.refresh(user2)

        response = self.client.get('amttest/api/user')
        self.assert200(response, 'getting users should return a 200')
        self.assertEqual(len(response.json), 2, 'get not returning all values')
        user1.archive = True
        db.session.commit()
        response_archive = self.client.get('amttest/api/user')
        self.assert200(response_archive, 'should get 200 even when archived users')
        self.assertEqual(len(response_archive.json), 1, 'get seems to return archived users')


    def test_add_user(self):
        response_no_header = self.client.post('amttest/api/user')
        self.assert400(response_no_header, 'post should require a token')

        response_no_data = self.client.post('amttest/api/user', headers=self.header_dict)
        self.assert400(response_no_data, 'some data is required for a new user')

        data = {'fbuserid': 'abc123',
                'name': 'test user',
                'email': 'test@test.test'}

        new_user = self.client.post('amttest/api/user', data=json.dumps(data), headers=self.header_dict)
        self.assertEqual(new_user.status_code, 201, 'post response returned no data')

        repete_user = self.client.post('amttest/api/user', data=json.dumps(data), headers=self.header_dict)
        self.assert200(repete_user, 'existing fbuserid should return a 200, existing user')
        user = User.query.filter_by(userid=new_user.json['userid']).first()
        self.assertTrue(user, 'user does not exist in database after post')
        user_dict = table2dict(user)
        self.compare_user(new_user.json, user_dict)

        data.pop('name')
        data['fbuserid'] = 'abcdefg'
        missing_data = self.client.post('amttest/api/user', data=json.dumps(data), headers=self.header_dict)
        self.assert400(missing_data, 'user should not be created with out all required fields')

        data['name'] = 'test user'
        data['kingdom'] = 'IMD'
        data['amt_name'] = 'toaster' #no idea

        extra_data = self.client.post('amttest/api/user', data=json.dumps(data), headers=self.header_dict)
        user2 = User.query.filter_by(userid=extra_data.json['userid']).first()
        user2_dict = table2dict(user2)
        self.compare_user(extra_data.json, user2_dict)
        self.assertEqual(user2_dict['kingdom'], data['kingdom'])


    def test_put_user(self):
        response_no_header = self.client.put('amttest/api/user/42')
        self.assert400(response_no_header, 'post should require a token')

        response_no_data = self.client.put('amttest/api/user/42', headers=self.header_dict)
        self.assert400(response_no_data, 'some data is required for a new user')

        user1 = User(name='test1', fbuserid='test123',
                     email='test1@test1.test1')
        db.session.add(user1)
        db.session.commit()
        db.session.refresh(user1)

        update_data = {'kingdom': 'IMD'}

        response_no_user = self.client.put('amttest/api/user/42', data=json.dumps(update_data),
                                           headers=self.header_dict)
        self.assert400(response_no_user, 'should return 400 when user does not exist')

        basic_update = self.client.put('amttest/api/user/1', data=json.dumps(update_data), headers=self.header_dict)
        self.assertEqual(basic_update.status_code, 204, 'basic update failed')
        query_user = User.query.filter_by(userid=1, archive=False).first()
        user1_dict = table2dict(query_user)
        print(user1_dict['kingdom'])
        print(update_data['kingdom'])
        self.assertEqual(user1_dict['kingdom'], update_data['kingdom'], 'update does not save changes')

        dummy_data = {'something': 'peanut'}
        update_bad_data = self.client.put('amttest/api/user/1', data=json.dumps(dummy_data), headers=self.header_dict)
        self.assertEqual(update_bad_data.status_code, 204, 'update, random data failed')
        user1_dict_update = table2dict(user1)
        self.assertEqual(user1_dict, user1_dict_update, 'dummy fields updated the user')


    def test_delete_user(self):
        response_no_header = self.client.delete('amttest/api/user/42')
        self.assert400(response_no_header, 'delete should require a token')

        response_empty = self.client.delete('amttest/api/user/42', headers=self.header_dict)
        self.assert400(response_empty, 'requesting a missing user should fail')
        user1 = User(name='test1', fbuserid='test123',
                     email='test1@test1.test1')

        db.session.add(user1)
        db.session.commit()
        db.session.refresh(user1)

        response_delete = self.client.delete('amttest/api/user/1', headers=self.header_dict)
        self.assertEqual(response_delete.status_code, 204, 'delete should return a 204')
        db.session.refresh(user1)
        self.assertTrue(user1.archive, 'user should be archived')


    def compare_user(self, response_user, db_user):
        for field in response_user.keys():
            self.assertEqual(response_user[field], db_user[field], 'response and database user do not match')