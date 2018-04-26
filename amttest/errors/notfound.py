from .apierror import APIError
from ..helpers.bphandler import BPHandler

from flask import make_response, Blueprint

NOT_FOUND_BP = Blueprint('NotFound', __name__)
BPHandler.add_blueprint(NOT_FOUND_BP, url_prefix='/amttest/api')

class NotFound(APIError):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.code = 404
        self.error = 'Page Not Found'


@NOT_FOUND_BP.app_errorhandler(NotFound)
def handle_not_found(error):
    return make_response(error.to_json(), error.code)


@NOT_FOUND_BP.app_errorhandler(404)
def handle_404(error):
    not_found = NotFound(message=str(error))
    return make_response(not_found.to_json(), not_found.code)