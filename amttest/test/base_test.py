import json

from flask import Flask
from flask_testing import TestCase

from ..database import db
from ..database.utils import table2dict
from ..errors import *
from ..routes import *

from ..helpers import token
from ..helpers.bphandler import BPHandler

class BaseTest(TestCase):

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


    def default_get(self, route, db_object):
        self.add_obj_to_db([db_object])

        response = self.client.get('%s/1' % route)
        self.assert200(response, 'success status code not 200')

        record = table2dict(db_object)
        self.compare_object(response.json, record)

        response = self.client.get('%s/42' % route)
        self.assert400(response, 'non existent route should return 400')

        db_object.archive = True
        db.session.commit()
        db.session.refresh(db_object)

        response = self.client.get('%s/1' % route)
        self.assert400(response, 'archived values should not return')


    def default_get_all(self, route, object_list):
        response_empty = self.client.get(route)
        self.assert200(response_empty,
                       'even an emptry respones should return values')
        self.assertListEqual(response_empty.json, [])
        self.add_obj_to_db(object_list)

        response = self.client.get(route)
        self.assert200(response, 'getting values should return a 200')
        self.assertEqual(len(response.json), 2, 'get not returning all values')

        object_list[0].archive = True
        db.session.commit()

        response_archive = self.client.get(route)
        self.assert200(response_archive,
                       'should get 200 even when archived values')
        self.assertEqual(len(response_archive.json), len(object_list) -1,
                         'get seems to return archived values')


    def default_put(self, route, payload, db_obj, table):
        response_no_header = self.client.put('%s/42' % route)
        self.assert400(response_no_header, 'post should require a token')

        response_no_data = self.client.put('%s/42' % route, headers=self.header_dict)
        self.assert400(response_no_data, 'some data is required for a new entry')

        self.add_obj_to_db([db_obj])

        response_no_value = self.client.put('%s/42' % route, data=json.dumps(payload),
                                           headers=self.header_dict)
        self.assert400(response_no_value, 'should return 400 when key does not exist')

        basic_update = self.client.put('%s/1' % route, data=json.dumps(payload), headers=self.header_dict)
        self.assertEqual(basic_update.status_code, 204, 'basic update failed')
        query_obj = table.query.filter_by(archive=False).all()[0]
        obj_dict = table2dict(query_obj)

        self.assertEqual(obj_dict[list(payload.keys())[0]], payload[list(payload.keys())[0]], 'update does not save changes')

        dummy_data = {'something': 'peanut'}

        update_bad_data = self.client.put('%s/1' % route, data=json.dumps(dummy_data), headers=self.header_dict)
        self.assertEqual(update_bad_data.status_code, 204, 'update, random data failed')
        dict_update = table2dict(db_obj)
        self.assertEqual(obj_dict, dict_update, 'dummy fields updated the database')


    def default_post(self, route, payload, table):
        response_no_header = self.client.post(route)
        self.assert400(response_no_header, 'post should require a token')

        response_no_data = self.client.post(route,
                                            headers=self.header_dict)
        self.assert400(response_no_data, 'some data is required for a new object')

        new_entry = self.client.post(route, data=json.dumps(payload),
                                    headers=self.header_dict)
        self.assertEqual(new_entry.status_code, 201,
                         'post response returned no data')

        db_obj = table.query.all()[0]
        self.assertTrue(db_obj, 'object does not exist in database after post')
        obj_dict = table2dict(db_obj)
        self.compare_object(new_entry.json, obj_dict)


    def default_delete(self, route, db_object):
        response_no_header = self.client.delete('%s/42' % route)
        self.assert400(response_no_header, 'delete should require a token')

        response_empty = self.client.delete('%s/42' % route, headers=self.header_dict)
        self.assert400(response_empty, 'requesting a missing payload should fail')

        db.session.add(db_object)
        db.session.commit()
        db.session.refresh(db_object)

        response_delete = self.client.delete('%s/1' % route, headers=self.header_dict)
        self.assertEqual(response_delete.status_code, 204, 'delete should return a 204')
        db.session.refresh(db_object)
        self.assertTrue(db_object.archive, 'entry should be archived')


    def compare_object(self, response_dict, db_dict):
        for field in response_dict.keys():
            self.assertEqual(response_dict[field], db_dict[field], 'response and database do not match')


    def add_obj_to_db(self, object_list):
        for db_object in object_list:
            db.session.add(db_object)
            db.session.commit()
            db.session.refresh(db_object)
