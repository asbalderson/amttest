""" Test all routes for User creation, modification, and query."""

import json

from .base_test import BaseTest

from ..database.utils import table2dict
from ..database.tables.user import User
from ..errors import badrequest, forbbiden, gone, internalservererror, \
    methodnotallowed, notfound, unauthorized
from ..routes import user


class TestUser(BaseTest):
    """ Class based on UnitTest.TestCase for testing user routes. """

    def create_app(self):
        """ Configure and stand up the flask app for testing. """
        return BaseTest.create_app(self)

    def setUp(self):
        """ Create a database for testing. """
        BaseTest.setUp(self)

    def tearDown(self):
        """ Delete the database used during testing. """
        BaseTest.tearDown(self)

    def test_get_user(self):
        """ Tests for querying a single user. """
        user1 = User(name='test', fbuserid='abc123', email='test@test.test')
        self.default_get('amttest/api/user', user1)

    def test_get_all_users(self):
        """ Tests for querying all users. """
        user1 = User(name='test1',
                     fbuserid='test123',
                     email='test1@test1.test1')
        user2 = User(name='test2',
                     fbuserid='testabc',
                     email='test2@test2.test2')
        user_list = [user1, user2]
        self.default_get_all('amttest/api/user', user_list)

    def test_add_user(self):
        """ Tests for route to add users. """
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
                       'user should not be created with '
                       'out all required fields')
        payload['name'] = 'test user'

        payload['kingdom'] = 'IMD'
        payload['amt_name'] = 'toaster'  # no idea

        extra_data = self.client.post('amttest/api/user',
                                      data=json.dumps(payload),
                                      headers=self.header_dict)

        user2 = User.query.filter_by(userid=extra_data.json['userid']).first()
        user2_dict = table2dict(user2)

        self.compare_object(extra_data.json, user2_dict)
        self.assertEqual(user2_dict['kingdom'], payload['kingdom'])

    def test_put_user(self):
        """ Test for the route to modify a user. """
        payload = {'kingdom': 'IMD'}

        user1 = User(name='test1', fbuserid='test123',
                     email='test1@test1.test1')
        self.default_put('amttest/api/user', payload, user1, User)

    def test_delete_user(self):
        """ Test for the route to delete (archive) a user. """
        user1 = User(name='test1', fbuserid='test123',
                     email='test1@test1.test1')
        self.default_delete('amttest/api/user', user1)
