from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

from ..database import db
from ..database.utils import table2dict
from ..database.tables.answer import Answer

from ..errors.badrequest import BadRequest

import json
import logging

ANSWER_BP = Blueprint('answer', __name__)
BPHandler.add_blueprint(ANSWER_BP, url_prefix='/amttest/api')


@ANSWER_BP.route('/question/<int:question_id>/answer', methods=['POST'])
def add_answer(question_id):
    check_token(get_token(request))
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    answer = {}
    required = ['answer', 'correct']
    for field in payload.keys():
        if field in required:
            required.remove(field)
        if field in inspect(Answer).mapper.column_attrs:
           answer[field] = payload[field]

    if required:
        raise BadRequest('missing all required fields: %s' % required)

    new = Answer(**answer)
    db.session.add(new)
    db.session.commit()
    db.session.refresh(new)

    return make_response(jsonify(table2dict(new)), 201)


@ANSWER_BP.route('/answer/<int:answer_id>', methods=['GET'])
def get_answer(answer_id):
    answer = Answer.query.filter_by(archive=False, answerid=answer_id)
    if not answer:
        raise BadRequest('Answer not found')
    return make_response(jsonify(table2dict(answer)), 200)


@ANSWER_BP.route('/answer/<int:answer_id>', methods=['PUT'])
def update_answer(answer_id):
    check_token(get_token(request))
    answer = Answer.query.filter_by(archive=False, answerid=answer_id)
    if not answer:
        raise BadRequest('Answer not found')
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    for field in payload.keys():
        if field in inspect(Answer).mapper.column_attrs:
            setattr(answer, field, payload[field])

    db.session.commit()
    return make_response('', 204)


@ANSWER_BP.route('/answer/<int:answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    check_token(get_token(request))
    answer = Answer.query.filter_by(archive=False, answerid=answer_id)
    if not answer:
        raise BadRequest('Answer not found')
    answer.archive = True
    db.session.commit()

    return make_response('', 204)
