from .apierror import APIError
from ..helpers.bphandler import BPHandler

from flask import make_response, Blueprint

GONE_BP = Blueprint('Gone', __name__)
BPHandler.add_blueprint(GONE_BP, url_prefix='/amttest/api')

class Gone(APIError):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.code = 410
        self.error = 'Gone'


@GONE_BP.app_errorhandler(Gone)
def handle_gone(error):
    return make_response(error.to_json())


@GONE_BP.app_errorhandler(410)
def handle_410(error):
    not_found = Gone(message=str(error))
    return make_response(not_found.to_json())