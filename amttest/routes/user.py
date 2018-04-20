from flask import jsonify, request, make_response, Blueprint

from ..errors.badrequest import BadRequest
from ..helpers.bphandler import BPHandler

USER_BP = Blueprint('user', __name__)
BPHandler.add_blueprint(USER_BP, url_prefix='/amttest/api')
#this data is temproary for test data
users = [
    {
        'fburserid':12345678,
        'amtname': 'baconman',
        'fbname': 'super bacon',
        'email': 'bacon@bacon.bacon',
        'userid': 1
    },
]

@USER_BP.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    """
    gets user data to be parsed and/or displayed on the admin page
    return: literally everything in the users table, see line 21
            but should probably return only the non expired most
            recent test result for each user.
    """

    global user
    return make_response(jsonify(user), 200)


@USER_BP.route('/users', methods = ['POST'])
def create_user():
    """
    creates a shell of a user, with their uid, amtname, name, and email
    args:
        {
            "amtname": "example",
            "email": "example@amtgard.com",
            "name": "jane doe",
            "userid": "is this email?"
        }
    """
    user_shell = {}
    bad = {}
    for arg in ['amtname', 'email', 'name', 'userid']:
        value = request.args.get(arg)
        if value:
            user_shell[arg] = value
        else:
            bad[arg] = value
    if bad:
        raise BadRequest('not all required values suplied', **bad)


    return make_response({'status': 'success'}, 201)

@USER_BP.route('/users/<int:user_uid>', methods = ['PUT'])
def put_update_user(user_uid):
    """
    updates user with new information, generally after a user has submitted a test,
    uid is required, whatever information is being updated should be included
    {
        "uid": "whatever this is",
        "email": "jane.doe@example.com",
    }

    """
    global user
    return make_response(jsonify(user), 201)


@USER_BP.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    """
    removes a user, probably because something went wrong :)
    user will actually be archived
    """
    result = {}
    result['success'] = True
    result['message'] = 'user %s Deleted' % user_id
    return make_response(jsonify(result), 200)
