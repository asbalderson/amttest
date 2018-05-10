"""Base test class for testing get, put, pull, and delete routes."""

import json

from flask import Flask
from flask_testing import TestCase

from ..database import DB
from ..database.utils import table2dict
from ..errors import badrequest, forbbiden, gone, internalservererror, \
    methodnotallowed, notfound, unauthorized
from ..helpers import token
from ..helpers.bphandler import BPHandler
from ..routes import answer, certificate, exam, question, section, user


class BaseTest(TestCase):
    """
    Class for standing up a flask app and database for testing.

    It also has methods for testing get, get_all, post, put, and delete.
    """

    def create_app(self):
        """Create a flask ap, and empty sqlite database in memory."""
        app = Flask('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        BPHandler.register_blueprints(app)
        DB.app = app
        DB.init_app(app)
        return app

    def setUp(self):
        """Create the tables for testing, and create a token for writing."""
        DB.create_all()
        this_token = token.gen_token()
        self.header_dict = {'token': this_token}

    def tearDown(self):
        """Delete the database, clearing all the data."""
        DB.session.remove()
        DB.drop_all()

    def default_get(self, route, db_object, ignore=None):
        """
        Run a set of tests involving a get on of a single item.

        Tests include:
            success returns a 200
            result object is the same as the database data
            bad routes raise a bad request, 400
            archived values do not appear
        :param route: string, base path of the route
        :param db_object: SQLAlchemy.database.model, object the get queries
        :param ignore: list, keys not returned from the get
        :return: None
        """
        self.add_obj_to_db([db_object])

        response = self.client.get('%s/1' % route)
        self.assert200(response, 'success status code not 200')

        record = table2dict(db_object)
        if ignore:
            for thing in ignore:
                response.json.pop(thing)

        self.compare_object(response.json, record)

        response = self.client.get('%s/42' % route)
        self.assert400(response, 'non existent route should return 400')

        db_object.archive = True
        DB.session.commit()
        DB.session.refresh(db_object)

        response = self.client.get('%s/1' % route)
        self.assert400(response, 'archived values should not return')

    def default_get_all(self, route, object_list):
        """
        Test for getting all objects from a route.

        Tests include:
            200 result even if no data
            response 200 when data exists
            number of objects in a response match the number in the database
            archived values do not return in the get all
        :param route: String, path to the route.
        :param object_list: list of database entires to add to the database.
        :return: None
        """
        response_empty = self.client.get(route)
        self.assert200(response_empty,
                       'even an emptry respones should return values')
        self.assertListEqual(response_empty.json, [])
        self.add_obj_to_db(object_list)

        response = self.client.get(route)
        self.assert200(response, 'getting values should return a 200')
        self.assertEqual(len(response.json), len(object_list),
                         'get not returning all values')

        object_list[0].archive = True
        DB.session.commit()

        response_archive = self.client.get(route)
        self.assert200(response_archive,
                       'should get 200 even when archived values')
        self.assertEqual(len(response_archive.json), len(object_list) - 1,
                         'get seems to return archived values')

    # pylint: disable=R0913
    def default_put(self, route, payload, db_obj, table, ignore=None):
        """
        Test a put route, confirming the payload is input in the database.

        Tests include:
            put has a token
            there is a payload in the request
            400 when there is no entry
            a payload properly updates the database
            a payload with stupid data does not raise an error
            values in the ignore, list, do not update the database
        :param route: string, route to the put request
        :param payload: dict, data to update during the put
        :param db_obj: SQLAlchemy.database.model, database value getting
                        modified.
        :param table: SQLAlchemy.database.model, actual database table object.
        :param ignore: dict, values that should not get updated during a put.
        :return: None
        """
        response_no_header = self.client.put('%s/42' % route)
        self.assert400(response_no_header, 'post should require a token')

        response_no_data = self.client.put('%s/42' % route,
                                           headers=self.header_dict)
        self.assert400(response_no_data,
                       'some data is required for a new entry')

        self.add_obj_to_db([db_obj])

        response_no_value = self.client.put('%s/42' % route,
                                            data=json.dumps(payload),
                                            headers=self.header_dict)
        self.assert400(response_no_value,
                       'should return 400 when key does not exist')

        basic_update = self.client.put('%s/1' % route,
                                       data=json.dumps(payload),
                                       headers=self.header_dict)
        self.assertEqual(basic_update.status_code, 204, 'basic update failed')
        query_obj = table.query.filter_by(archive=False).all()[0]
        obj_dict = table2dict(query_obj)

        self.assertEqual(obj_dict[list(payload.keys())[0]],
                         payload[list(payload.keys())[0]],
                         'update does not save changes')

        dummy_data = {'something': 'peanut'}

        update_bad_data = self.client.put('%s/1' % route,
                                          data=json.dumps(dummy_data),
                                          headers=self.header_dict)
        self.assertEqual(update_bad_data.status_code, 204,
                         'update, random data failed')
        dict_update = table2dict(db_obj)
        self.compare_object(obj_dict, dict_update)

        if ignore:
            for k, val in ignore.items():
                payload[k] = val
                self.client.put('%s/1' % route,
                                data=json.dumps(payload),
                                headers=self.header_dict)
                data = table2dict(db_obj)
                self.assertNotEqual(data[k], val,
                                    'should not be able to update ignore '
                                    'value %s' % k)
                payload.pop(k)

    def default_post(self, route, payload, table, ignore=None):
        """
        Test a post route, ensuring the value is added to the database.

        Tests include:
            400 if no token
            400 if no data
            201 if value entered
            value is in the database
            value in the database matches the payload
            database does not update values in the ignore list
        :param route: string, route to the post request
        :param payload: dict, data to update during the post
        :param table: SQLAlchemy.database.model, actual database table object.
        :param ignore: dict, values that should not get updated during a post.
        :return: None
        """
        response_no_header = self.client.post(route)
        self.assert400(response_no_header, 'post should require a token')

        response_no_data = self.client.post(route,
                                            headers=self.header_dict)
        self.assert400(response_no_data,
                       'some data is required for a new object')

        new_entry = self.client.post(route, data=json.dumps(payload),
                                     headers=self.header_dict)
        self.assertEqual(new_entry.status_code, 201,
                         'post response returned no data')

        db_obj = table.query.all()[0]
        self.assertTrue(db_obj, 'object does not exist in database after post')
        obj_dict = table2dict(db_obj)
        self.compare_object(new_entry.json, obj_dict)

        if ignore:
            for k, val in ignore.items():
                payload[k] = val
                response_ignore = self.client.post(route,
                                                   data=json.dumps(payload),
                                                   headers=self.header_dict)
                self.assertNotEqual(response_ignore.json[k], val,
                                    'should not be able to update ignore '
                                    'value %s' % k)
                payload.pop(k)

    def default_delete(self, route, db_object):
        """
        Test a delete route, ensuring it works correctly.

        Tests include:
            400 if no token
            400 if object not in database
            204 when archive successful
            value is actually archived after running
        :param route: String, path to the route
        :param db_object: SQLAlchemy.database.model, database value getting
                        deleted.
        :return: None
        """
        response_no_header = self.client.delete('%s/42' % route)
        self.assert400(response_no_header, 'delete should require a token')

        response_empty = self.client.delete('%s/42' % route,
                                            headers=self.header_dict)
        self.assert400(response_empty, 'requesting a bad id should fail')

        DB.session.add(db_object)
        DB.session.commit()
        DB.session.refresh(db_object)

        response_delete = self.client.delete('%s/1' % route,
                                             headers=self.header_dict)
        self.assertEqual(response_delete.status_code, 204,
                         'delete should return a 204')
        DB.session.refresh(db_object)
        self.assertTrue(db_object.archive, 'entry should be archived')

    def compare_object(self, response_dict, db_dict):
        """
        Compare values in response.json and the database values.

        :param response_dict: response.json: data from the response
        :param db_dict: dict, a dict representing a database row
        :return: None
        """
        for field in response_dict.keys():
            self.assertEqual(response_dict[field], db_dict[field],
                             'response and database do not match')

    @staticmethod
    def add_obj_to_db(object_list):
        """
        Add a list of database row's to the database.

        :param object_list: List of SQLAlchemy.database.model instances
        :return: None
        """
        for db_object in object_list:
            DB.session.add(db_object)
            DB.session.commit()
            DB.session.refresh(db_object)
