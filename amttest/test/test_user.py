import json

from .base_test import BaseTest

from ..database import db
from ..database.utils import table2dict
from ..database.tables.user import User
from ..errors import *
from ..routes import user


class TestUser(BaseTest):

    def create_app(self):
        return BaseTest.create_app(self)


    def setUp(self):
        BaseTest.setUp(self)


    def tearDown(self):
        BaseTest.tearDown(self)


    def test_get_user(self):
        user = User(name='test', fbuserid='abc123', email='test@test.test')
        self.default_get('amttest/api/user', user)


    def test_get_all_users(self):
        user1 = User(name='test1', fbuserid='test123', email='test1@test1.test1')
        user2 = User(name='test2', fbuserid='testabc', email='test2@test2.test2')
        user_list = [user1, user2]
        self.default_get_all('amttest/api/user', user_list)


    def test_add_user(self):
        payload = {'fbuserid': 'abc123',
                'name': 'test user',
                'email': 'test@test.test'}

        self.default_post('amttest/api/user', payload, User)

        repeat_user = self.client.post('amttest/api/user',
                                       data=json.dumps(payload),
                                       headers=self.header_dict)
        self.assert200(repeat_user,
                       'existing fbuserid should return a 200, existing user')
        payload.pop('name')
        payload['fbuserid'] = 'abcdefg'
        missing_data = self.client.post('amttest/api/user',
                                        data=json.dumps(payload),
                                        headers=self.header_dict)
        self.assert400(missing_data,
                       'user should not be created with out all required fields')
        payload['name'] = 'test user'

        payload['kingdom'] = 'IMD'
        payload['amt_name'] = 'toaster'  # no idea

        extra_data = self.client.post('amttest/api/user', data=json.dumps(payload),
                                      headers=self.header_dict)

        user2 = User.query.filter_by(userid=extra_data.json['userid']).first()
        user2_dict = table2dict(user2)

        self.compare_object(extra_data.json, user2_dict)
        self.assertEqual(user2_dict['kingdom'], payload['kingdom'])


    def test_put_user(self):
        payload = {'kingdom': 'IMD'}

        user = User(name='test1', fbuserid='test123',
                     email='test1@test1.test1')
        self.default_put('amttest/api/user', payload, user, User)


    def test_delete_user(self):
        user1 = User(name='test1', fbuserid='test123',
                     email='test1@test1.test1')
        self.default_delete('amttest/api/user', user1)
