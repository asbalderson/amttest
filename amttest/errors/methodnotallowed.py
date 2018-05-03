from .apierror import APIError
from ..helpers.bphandler import BPHandler

from flask import make_response, Blueprint

METHOD_NOT_ALLOWED_BP = Blueprint('Method Not Allowed', __name__)
BPHandler.add_blueprint(METHOD_NOT_ALLOWED_BP, url_prefix='/amttest/api')


class MethodNotAllowed(APIError):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.code = 405
        self.error = 'Method Not Allowed'


@METHOD_NOT_ALLOWED_BP.app_errorhandler(MethodNotAllowed)
def handle_message_not_allowed_error(error):
    return make_response(error.to_json(), error.code)


@METHOD_NOT_ALLOWED_BP.app_errorhandler(405)
def handle_405(error):
    err = MethodNotAllowed(message=str(error))
    return make_response(err.to_json(), err.code)
