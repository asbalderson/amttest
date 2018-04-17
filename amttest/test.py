import logging

from flask import jsonify, request, make_response, Blueprint

from .errors.badrequest import BadRequest

tests = [

    {
        'name': u'rules of engagement',
        'passing score': u'75',
        'time limit': u'60m',
        'expires': u'2y',
        'user agreement': 'i agree that this test was taken honestly blah blah...',
        'sections': {
                        u'example_section':2,
                        u'miscellaneous':1
                    }
    },

    {
        'name': u'rules of engagement',
        'passing score': u'75',
        'time limit': u'60m',
        'expires': u'2y',
        'sections': {u'example_section':2,
                     u'miscellaneous':1}
    }

]

TEST_BP = Blueprint('test', __name__)

@TEST_BP.route('/tests/<int:test_id>', methods = ['GET'])
def get_test(test_id):
    """
    returns the test information, including all the sections, question counts
    form each section, time limits, etc.

    also need to to flag the test as grabed once before, so it cant be grabbed again
    """
    msg = {
        'message': 'this fucking thing is so long, im not setting it up right now'
    }
    return make_response(jsonify(msg), 200)


@TEST_BP.route('/tests/<string:test_name>', methods = ['POST'])
def create_test(test_name):
    """
    creates a test which can be taken by users, questions will be
    random from a given sections (and probably in a random order too) and
    answers will also come in a random order.  the formatting on this is the
    key to the whole project
    """

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
    result = {}
    result['success'] = True
    result['message'] = 'test %s Deleted' % test_id
    return make_response(jsonify(result), 200)
