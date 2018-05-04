from ..database import db
from ..database.tables.token import Token

from ..errors.badrequest import BadRequest
from ..errors.unauthorized import Unauthorized

import logging
import random
import string


def gen_token(length=40):
    """
    Create a new token used to verify a user has write permission.
    Once the new token is generated, it is saved to the database.
    :param length: Integer, length of a token to generate
    :return: None
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    token = ''
    logger.debug('Generating new token length %s', length)
    for i in range(length):
        token += random.choice(string.ascii_letters + string.digits)
    this = Token(token=token)
    db.session.add(this)
    db.session.commit()
    logger.info('created token')
    logger.info(token)
    return token


def list_token():
    """
    List all current tokens in the database
    :return: None
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    result = Token.query.all()
    for token in result:
        logger.info(token.token)


def check_token(token):
    """
    Check if a token exists in the database
    :param token: String, a string of characters used as an API token
    :return: Boolean, true if the api token exists in the database
    """
    result = Token.query.filter_by(token=token).first()
    if result:
        return True
    raise Unauthorized('Bad API token')


def get_token(request):
    """
    Get an API token from a flask.request object
    :param request: flask.request: a request from a http(s) request
    :return: String, token used ot authenticate api requests
    """
    token = request.headers.get('Token')
    if not token:
        raise BadRequest(message='API token not provided')
    return token
