"""Routes related to a the user table."""
import logging

from flask import jsonify, request, make_response, Blueprint

from . import get_payload

from ..database import DB
from ..database.tables.user import User
from ..database.utils import add_value, table2dict
from ..errors.badrequest import BadRequest
from ..errors.notfound import NotFound
from ..helpers.bphandler import BPHandler
from ..helpers.token import check_token, get_token

USER_BP = Blueprint('user', __name__)
BPHandler.add_blueprint(USER_BP)


@USER_BP.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get all info about a single user."""
    check_token(get_token(request))
    user = query_userid(user_id)

    data = table2dict(user)
    return make_response(jsonify(data), 200)


@USER_BP.route('/user', methods=['GET'])
def get_all_users():
    """Get data on all users."""
    check_token(get_token(request))
    all_users = User.query.filter_by(archive=False).all()
    returnlist = []
    for user in all_users:
        tmp = table2dict(user)
        returnlist.append(tmp)

    return make_response(jsonify(returnlist), 200)


@USER_BP.route('/user', methods=['POST'])
def create_user():
    """Create a single user."""
    logger = logging.getLogger(__name__)
    check_token(get_token(request))
    required = ['name', 'email']
    possible = ['amtname', 'kingdom', 'admin'] + required
    ignore = ['archive', 'userid']
    payload = get_payload(request)

    unused = {}
    user = {}
    for field in payload.keys():
        if field in ignore:
            continue
        if field == 'email':
            exists = User.query.filter_by(email=payload[field].lower()).first()
            if exists:
                return make_response(jsonify(table2dict(exists)), 200)
            required.remove(field)
            possible.remove(field)
            user[field] = payload[field].lower()
        elif field in required:
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
    if new.userid == 1:
        new.admin = True
    DB.session.refresh(new)
    return make_response(jsonify(table2dict(new)), 201)


@USER_BP.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a single user."""
    logger = logging.getLogger(__name__)
    check_token(get_token(request))
    payload = get_payload(request)
    ignore = ['archive', 'userid', 'email']
    user = query_userid(user_id)

    ignored = {}
    for field in payload.keys():
        if field in ignore:
            continue
        if field not in table2dict(user).keys():
            ignored[field] = payload[field]
        else:
            setattr(user, field, payload[field])

    DB.session.commit()

    return make_response('', 204)


@USER_BP.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Set a users archive flag to True, removing it from queries."""
    logger = logging.getLogger(__name__)
    check_token(get_token(request))

    user = query_userid(user_id)

    logger.info(user)
    user.archive = True
    DB.session.commit()

    return make_response('', 204)


def query_userid(userid):
    """
    Get a user based on its userid, or raise a BadRequest if not found.

    :param userid: int, primary key for a single user.
    :return: Table data on a single user.
    """
    user = User.query.filter_by(userid=userid, archive=False).first()
    if not user:
        raise NotFound(message='User not found')
    return user
