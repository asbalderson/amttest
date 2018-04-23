from flask import jsonify, request, make_response, Blueprint

from ..helpers.bphandler import BPHandler
from ..helpers.token import check_token, get_token

CERT_BP = Blueprint('certificate', __name__)
BPHandler.add_blueprint(CERT_BP, url_prefix='/amttest/api')

certifications =  [
    {
        'userid': 1,
        'testid': 123456,
        'test_name': u'rules of engagement',
        'correct': 20,
        'possible': 25,
        'testdate': u'8/22/2017',
        'passed': True
    },
    {
        'userid': 2,
        'testid': 424242,
        'name': u'tournament rules',
        'correct': 20,
        'possible': 25,
        'testdate': u'3/29/2016',
        'passed': True
    },
]


@CERT_BP.route('/certificate/<int:user_uid>/<int:test_id>', methods = ['POST'])
def update_certificate(user_uid, test_id):
    """
    adds a new test result to the users certificate.  date can be auto gnerated
    so the only missing information is the users score since pass fail can be
    calculated on the fly and dropped in.
    """
    check_token(get_token(request))

    message = {}
    message['correct'] = 20
    message['possible'] = 25
    return make_response(jsonify(message), 201)


@CERT_BP.route('/certificate/<int:user_uid>/<int:test_id>', methods = ['GET'])
def get_certificate(user_uid, test_id):
    """
    adds a new test result to the users certificate.  date can be auto gnerated
    so the only missing information is the users score since pass fail can be
    calculated on the fly and dropped in.
    """
    message = {}
    message['correct'] = 20
    message['possible'] = 25
    return make_response(jsonify(message), 200)


# does it make more sense to do /user/userid/certificates?
@CERT_BP.route('/certificate/<int:user_uid>', methods = ['GET'])
def get_user_certs(user_uid):
    """
     get all certificates for a given user
    """
    global certifications
    return make_response(jsonify(certifications[1]), 200)


@CERT_BP.route('/certificate/<int:test_id>', methods = ['GET'])
def get_test_certs(test_id):
    """
    get a cert for a specific testid
    :param test_id:
    :return:
    """
    global certifications
    return make_response(jsonify(certifications[0]), 200)


@CERT_BP.route('/certificate', methods = ['GET'])
def get_all_certs():
    """
    get all certs
    :return:
    """
    global certifications
    return make_response(jsonify(certifications), 200)