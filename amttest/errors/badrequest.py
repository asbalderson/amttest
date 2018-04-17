from .apierror import APIError
from ..helpers.bphandler import BPHandler

from flask import jsonify, make_response, Blueprint

BAD_REQUEST_BP = Blueprint('BadRequest', __name__)
BPHandler.add_blueprint(BAD_REQUEST_BP, url_prefix='/amttest/api')

class BadRequest(APIError):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.code = 400
        self.error = 'Bad Request'


@BAD_REQUEST_BP.app_errorhandler(BadRequest)
def handle_bad_request(message, **kwargs):
    error = BadRequest(message, **kwargs)
    print(error.to_json())
    return make_response(error.to_json())