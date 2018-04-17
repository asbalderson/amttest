from flask import jsonify, request, make_response, Blueprint

CERT_BP = Blueprint('certificate', __name__)

certifications =  [
    {
        'uid': 'whatever facebook says',
        'testid': 123456,
        'name': u'rules of engagement',
        'correct': u'20',
        'testdate': u'8/22/2017',
        'status': u'passed'
    },
    {
        'uid': 'whatever facebook says',
        'testid': 424242,
        'name': u'tournament rules',
        'correct': u'20',
        'testdate': u'3/29/2016',
        'status': u'passed'
    },
]


@CERT_BP.route('/certificate/<int:user_uid>/<int:test_id>', methods = ['POST'])
def update_certificate(user_uid, test_id):
    """
    adds a new test result to the users certificate.  date can be auto gnerated
    so the only missing information is the users score since pass fail can be
    calculated on the fly and dropped in.

    {
        "correct": 3
    }
    """
    message = {}
    message['correct'] = 20
    message['questions'] = 25
    return make_response(jsonify(message), 201)


# does it make more sense to do /user/userid/certificates?
@CERT_BP.route('/certificate/<int:user_uid>', methods = ['GET'])
def get_certs(user_uid):
    """
     get all certificates for a given user
    """
    global certifications
    return make_response(jsonify(certifications), 200)
