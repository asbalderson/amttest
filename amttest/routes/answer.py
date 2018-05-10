""" Routes for modifying the Answer table. """

import logging

from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from . import get_payload

from ..helpers.bphandler import BPHandler
from ..helpers.token import check_token, get_token
from ..database import DB
from ..database.utils import add_value, table2dict
from ..database.tables.answer import Answer
from ..errors.badrequest import BadRequest


ANSWER_BP = Blueprint('answer', __name__)
BPHandler.add_blueprint(ANSWER_BP, url_prefix='/amttest/api')


@ANSWER_BP.route('/question/<int:question_id>/answer', methods=['POST'])
def add_answer(question_id):
    """ Add a single answer to the database. """
    check_token(get_token(request))
    payload = get_payload(request)
    answer = {'questionid': question_id}
    required = ['answer', 'correct']
    ignore = ['answerid', 'archive', 'chosen']
    for field in payload.keys():
        if field in required:
            required.remove(field)
        if field in ignore:
            continue
        if field in inspect(Answer).mapper.column_attrs:
            answer[field] = payload[field]

    if required:
        raise BadRequest('missing all required fields: %s' % required)

    new = Answer(**answer)
    add_value(new)

    return make_response(jsonify(table2dict(new)), 201)


@ANSWER_BP.route('/answer/<int:answer_id>', methods=['GET'])
def get_answer(answer_id):
    """Get a single answer based on the answer id."""
    answer = query_answerid(answer_id)
    return make_response(jsonify(table2dict(answer)), 200)


@ANSWER_BP.route('/answer/<int:answer_id>', methods=['PUT'])
def update_answer(answer_id):
    """Update an answer based on its answer id."""
    check_token(get_token(request))
    answer = query_answerid(answer_id)
    payload = get_payload(request)
    ignore = ['answerid', 'archive', 'chosen']
    for field in payload.keys():
        if field in ignore:
            continue
        if field in inspect(Answer).mapper.column_attrs:
            setattr(answer, field, payload[field])

    DB.session.commit()
    return make_response('', 204)


@ANSWER_BP.route('/answer/<int:answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    """Set the archive flag to true, removing it from queries."""
    check_token(get_token(request))
    answer = query_answerid(answer_id)
    answer.archive = True

    DB.session.commit()
    return make_response('', 204)


def query_answerid(answer_id):
    """
    Get an answer based on the answerid or raise a BadRequest when not found.

    :param answer_id: int, primary key for the answer.
    :return: Table row representing an answer.
    """
    answer = Answer.query.filter_by(archive=False, answerid=answer_id).first()
    if not answer:
        raise BadRequest('Answer not found')
    return answer
