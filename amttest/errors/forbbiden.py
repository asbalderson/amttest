from .apierror import APIError
from ..helpers.bphandler import BPHandler

from flask import make_response, Blueprint

FORBIDDEN_BP = Blueprint('Forbidden', __name__)
BPHandler.add_blueprint(FORBIDDEN_BP, url_prefix='/amttest/api')

class Forbidden(APIError):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.code = 403
        self.error = 'Forbidden'


@FORBIDDEN_BP.app_errorhandler(Forbidden)
def handle_forbidden(error):
    return make_response(error.to_json())


@FORBIDDEN_BP.app_errorhandler(403)
def handle_403(error):
    not_found = Forbidden(message=str(error))
    return make_response(not_found.to_json())