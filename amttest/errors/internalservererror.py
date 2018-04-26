from .apierror import APIError
from ..helpers.bphandler import BPHandler

from flask import make_response, Blueprint

INTERNAL_SERVER_ERROR_BP = Blueprint('Internal Server Error', __name__)
BPHandler.add_blueprint(INTERNAL_SERVER_ERROR_BP, url_prefix='/amttest/api')

class InternalServerError(APIError):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.code = 500
        self.error = 'Internal Server Error'


@INTERNAL_SERVER_ERROR_BP.app_errorhandler(InternalServerError)
def handle_internal_server_error(error):
    return make_response(error.to_json(), error.code)


@INTERNAL_SERVER_ERROR_BP.app_errorhandler(500)
def handle_500(error):
    ise = InternalServerError(message=str(error))
    return make_response(ise.to_json(), ise.code)