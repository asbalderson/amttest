from .apierror import APIError
from ..helpers.bphandler import BPHandler

from flask import make_response, Blueprint

UNAUTHORIZED_BP = Blueprint('Unauthorized', __name__)
BPHandler.add_blueprint(UNAUTHORIZED_BP, url_prefix='/amttest/api')

class Unauthorized(APIError):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.code = 401
        self.error = 'Unauthorized'


@UNAUTHORIZED_BP.app_errorhandler(Unauthorized)
def handle_unauthorized(error):
    return make_response(error.to_json())