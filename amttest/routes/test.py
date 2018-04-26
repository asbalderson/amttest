import logging
import json

from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from ..errors.badrequest import BadRequest
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

from ..database import db
from ..database.utils import table2dict
from ..database.tables.test import Test


TEST_BP = Blueprint('test', __name__)
BPHandler.add_blueprint(TEST_BP, url_prefix='/amttest/api')


@TEST_BP.route('/tests', methods=['GET'])
def get_tests():
    """
    gets all tests which exists
    :return:
    """
    data = Test.query.filter_by(archive=False).all()
    return_list = []
    for test in data:
        return_list.append(table2dict(test))

    return make_response((jsonify(return_list)), 200)


@TEST_BP.route('/tests/<int:test_id>/take', methods = ['GET'])
def get_randomized_test(test_id):
    """
    returns a randomized test with a list of questions based on parameters set
    by the admin on test creation.
    :param test_id:
    :return:
    """
    #TODO :: add this method after all the other data can be populated
    msg = [
        {'questionid': 1234,
         'question':'yes?',
         'answers': [
             {'answerid': 2345,
              'answer': 'yes'},
             {'answerid': 2346,
              'answer': 'no'
             }
         ]},
        {'questionid': 1235,
         'question': 'up?',
         'answers': [
             {'answerid': 2347,
              'answer': 'up'},
             {'answerid': 2348,
              'answer': 'down'
              }
         ]}
    ]
    return make_response(jsonify(msg), 200)


@TEST_BP.route('/tests/<int:test_id>', methods = ['GET'])
def get_test(test_id):
    """
    returns the test information, and the section names and ids for that test

    also need to to flag the test as grabed once before, so it cant be grabbed again
    """
    test = Test.query.filter_by(archive=False, testid=test_id).first()
    if not test:
        raise BadRequest('test not found')
    return make_response(jsonify(table2dict(test)), 200)


@TEST_BP.route('/tests/', methods = ['POST'])
def create_test():
    """
    Creates a new test.
    """
    check_token(get_token(request))
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    tabledata = {}
    for column in payload.keys():
        if column not in inspect(Test).mapper.column_attrs:
            continue
        else:
            tabledata[column] = payload[column]

    test = Test(**tabledata)
    db.session.add(test)
    db.session.commit()
    db.session.refresh(test)

    return make_response(jsonify(table2dict(test)), 201)


@TEST_BP.route('/tests/<int:test_id>', methods = ['PUT'])
def update_test(test_id):
    """
    updates test if parameters need to be changed, things like
    name,
    """
    check_token(get_token(request))

    test = Test.query.filter_by(archive=False, testid=test_id).first()
    if not test:
        raise BadRequest('test not found')

    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    for field in payload.keys():
        if field in table2dict(test).keys():
            setattr(test, field, payload[field])

    db.session.commit()

    return make_response('', 204)


@TEST_BP.route('/tests/<int:test_id>', methods = ['DELETE'])
def delete_test(test_id):
    """
    removes a test (archive)
    """
    check_token(get_token(request))
    test = Test.query.filter_by(archive=False, testid=test_id).first()
    if not test:
        raise BadRequest('test not found')
    test.archive = True
    return make_response('', 204)
