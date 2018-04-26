from flask import jsonify, request, make_response, Blueprint

from ..database import db
from ..database.utils import table2dict
from ..database.tables.user import User
from ..errors.badrequest import BadRequest
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

import logging
import json

USER_BP = Blueprint('user', __name__)
BPHandler.add_blueprint(USER_BP, url_prefix='/amttest/api')


@USER_BP.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    """
    gets user data to be parsed and/or displayed on the admin page
    return: literally everything in the users table, see line 21
            but should probably return only the non expired most
            recent test result for each user.
    """
    user = query_userid(user_id)

    return make_response(jsonify(table2dict(user)), 200)


@USER_BP.route('/users', methods = ['POST'])
def create_user():
    """
    creates a shell of a user, with their uid, amtname, name, and email
    args:
    """
    logger = logging.getLogger(__name__)
    check_token(get_token(request))
    required = ['fbuserid', 'name', 'email']
    possible = ['amtname', 'kingdom'] + required
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    unused = {}
    user = {}
    for column in payload.keys():
        if column in required:
            required.remove(column)
            possible.remove(column)
            user[column] = payload[column]
        elif column in possible:
            possible.remove(column)
            user[column] = payload[column]
        else:
            unused[column] = payload[column]
    if required:
        raise BadRequest(message='Missing fields: %s' % required)

    new = User(**user)

    db.session.add(new)
    db.session.commit()
    db.session.refresh(new)

    return make_response(jsonify(table2dict(new)), 201)


@USER_BP.route('/users/<int:user_id>', methods = ['PUT'])
def put_update_user(user_id):
    """
    updates user with new information, generally after a user has submitted a test,
    uid is required, whatever information is being updated should be included
    {
        "uid": "whatever this is",
        "email": "jane.doe@example.com",
    }

    """
    logger = logging.getLogger(__name__)
    check_token(get_token(request))
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)

    user = query_userid(user_id)

    ignored = {}
    for field in payload.keys():
        if field not in table2dict(user).keys():
            ignored[field] = payload[field]
        else:
            setattr(user, field, payload[field])

    db.session.commit()

    return make_response('', 204)


@USER_BP.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    """
    removes a user, probably because something went wrong :)
    user will actually be archived
    """
    logger = logging.getLogger(__name__)
    check_token(get_token(request))

    user = query_userid(user_id)

    logger.info(user)
    user.archive = True
    db.session.commit()

    return make_response('', 204)


def query_userid(userid):
    user = User.query.filter_by(userid=user_id, archive=False).first()
    if not user:
        raise BadRequest(message='User not found')
    return user