from .apierror import APIError

from flask import jsonify, make_response, Blueprint
from werkzeug.exceptions import BadRequest

BAD_REQUEST_BP = Blueprint('BadRequest', __name__)

class AmtBadRequest(Exception):

    def __init__(self, message, **kwargs):
        #super().__init__(message, **kwargs)
        self.message = message
        if kwargs:
            self.__dict__.update(kwargs)
        self.code = 400
        self.error = 'Bad Request'

    def to_json(self):
        return jsonify(self.__dict__)


@BAD_REQUEST_BP.app_errorhandler(AmtBadRequest)
def handle_bad_request(message, **kwargs):
    error = AmtBadRequest(message, **kwargs)
    print(error.to_json())
    return make_response(error.to_json())