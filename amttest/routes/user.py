import logging

from flask import jsonify, request, make_response, Blueprint

from . import get_payload

from ..database import db
from ..database.tables.user import User
from ..database.utils import add_value, table2dict
from ..errors.badrequest import BadRequest
from ..helpers.bphandler import BPHandler
from ..helpers.token import check_token, get_token

USER_BP = Blueprint('user', __name__)
BPHandler.add_blueprint(USER_BP, url_prefix='/amttest/api')


@USER_BP.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    gets user data to be parsed and/or displayed on the admin page
    return: literally everything in the users table, see line 21
            but should probably return only the non expired most
            recent test result for each user.
    """
    user = query_userid(user_id)

    data = table2dict(user)
    data.pop('fbuserid')
    return make_response(jsonify(data), 200)


@USER_BP.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.filter_by(archive=False).all()
    returnlist = []
    for user in all_users:
        tmp = table2dict(user)
        tmp.pop('fbuserid')
        returnlist.append(tmp)

    return make_response(jsonify(returnlist), 200)


@USER_BP.route('/user', methods=['POST'])
def create_user():
    """
    creates a shell of a user, with their uid, amtname, name, and email
    args:
    """
    logger = logging.getLogger(__name__)
    check_token(get_token(request))
    required = ['fbuserid', 'name', 'email']
    possible = ['amtname', 'kingdom', 'admin'] + required
    ignore = ['archive', 'userid']
    payload = get_payload(request)

    unused = {}
    user = {}
    for field in payload.keys():
        if field in ignore:
            continue
        if field == 'fbuserid':
            exists = User.query.filter_by(fbuserid=payload[field]).first()
            if exists:
                return make_response(jsonify(table2dict(exists)), 200)
        if field in required:
            required.remove(field)
            possible.remove(field)
            user[field] = payload[field]
        elif field in possible:
            possible.remove(field)
            user[field] = payload[field]
        else:
            unused[field] = payload[field]
    if required:
        raise BadRequest(message='Missing fields: %s' % required)

    new = User(**user)

    add_value(new)
    return make_response(jsonify(table2dict(new)), 201)


@USER_BP.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    updates user with new information, generally after a user has submitted
    a test, uid is required, whatever information is being updated should be
    included
    {
        "uid": "whatever this is",
        "email": "jane.doe@example.com",
    }

    """
    logger = logging.getLogger(__name__)
    check_token(get_token(request))
    payload = get_payload(request)
    ignore = ['archive', 'userid']
    user = query_userid(user_id)

    ignored = {}
    for field in payload.keys():
        if field in ignore:
            continue
        if field not in table2dict(user).keys():
            ignored[field] = payload[field]
        else:
            setattr(user, field, payload[field])

    db.session.commit()

    return make_response('', 204)


@USER_BP.route('/user/<int:user_id>', methods=['DELETE'])
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
    user = User.query.filter_by(userid=userid, archive=False).first()
    if not user:
        raise BadRequest(message='User not found')
    return user
