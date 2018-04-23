import logging

from flask import jsonify, request, make_response, Blueprint

from ..errors.badrequest import BadRequest
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

tests = [

    {
        'name': u'rules of engagement',
        'pass_percent': 75,
        'time_limit': 60,
        'expiration': 1,
        'ula': 'i agree that this test was taken honestly blah blah...',
        'sections': {
                        u'example_section':2,
                        u'miscellaneous':1
                    }
    },

    {
        'name': u'rules of engagement',
        'pass_percent': 75,
        'time_limit': 60,
        'expiration': 1,
        'ula': 'i agree to NOTHING',
        'sections': {
                        u'example_section':2,
                        u'miscellaneous':1
                    }
    }

]

TEST_BP = Blueprint('test', __name__)
BPHandler.add_blueprint(TEST_BP, url_prefix='/amttest/api')

@TEST_BP.route('/tests/', methods=['GET'])
def get_tests():
    """
    gets all tests which exists
    :return:
    """
    global tests
    return make_response((jsonify(tests)), 200)


@TEST_BP.route('/tests/<int:test_id>/take', methods = ['GET'])
def get_randomized_test(test_id):
    """
    returns a randomized test with a list of questions based on parameters set
    by the admin on test creation.
    :param test_id:
    :return:
    """
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
    global test
    return make_response(jsonify(test), 200)


@TEST_BP.route('/tests/', methods = ['POST'])
def create_test():
    """
    creates a test which can be taken by users, questions will be
    random from a given sections (and probably in a random order too) and
    answers will also come in a random order.  the formatting on this is the
    key to the whole project
    """
    check_token(get_token(request))
    msg = {
        'message': 'test created successfuly',
        'testid': 123456,
    }
    return make_response(jsonify(msg), 201)


@TEST_BP.route('/tests/<int:test_id>', methods = ['PUT'])
def update_test(test_id):
     """
    updates test if parameters need to be changed, things like
    name, sections it takes questions from, number of questions in a section
    time limit, passing score, etc
    {
        "title": "ROP",
        "sections": {
                <section_id>:<questions from that section for the test>
        }
        "timelimit": 60
    }
    """
     check_token(get_token(request))
     global test
     bad = {}
     good = []
     for arg in request.args.keys():
         #TODO fix this its bullshit
         if arg in test.keys():
            good.append(arg)
         else:
             bad[arg] = request[arg]
     if bad:
         raise BadRequest('some values do not exist for tests', **bad)

     return make_response({}, 200)

@TEST_BP.route('/tests/<int:test_id>', methods = ['DELETE'])
def delete_test(test_id):
    """
    removes a test (archive)
    """
    check_token(get_token(request))
    result = {}
    result['success'] = True
    result['message'] = 'test %s Deleted' % test_id
    return make_response(jsonify(result), 200)
