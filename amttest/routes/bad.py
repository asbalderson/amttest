from flask import jsonify, request, make_response, Blueprint, abort

from ..helpers.bphandler import BPHandler

from ..errors.badrequest import BadRequest

BAD_BP = Blueprint('bad', __name__)
BPHandler.add_blueprint(BAD_BP, url_prefix='/amttest/api')

@BAD_BP.route('/bad', methods=['GET'])
def bad():
    #raise BadRequest('borked', thing='thing')
    raise Exception()