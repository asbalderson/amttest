import logging

from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from . import get_payload

from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token
from ..database import db
from ..database.utils import add_value, table2dict
from ..database.tables.question import Question
from ..database.tables.answer import Answer
from ..errors.badrequest import BadRequest


QUESTION_BP = Blueprint('question', __name__)
BPHandler.add_blueprint(QUESTION_BP, url_prefix='/amttest/api')


@QUESTION_BP.route('/section/<int:section_id>/question', methods=['POST'])
def create_question(section_id):
    """
    creates a new question under a section, question id's will probably all be
    unique but, it seems right to specify the section id every time. mongo
    can assign the question id
    """
    check_token(get_token(request))
    payload = get_payload(request)
    question = {'sectionid': section_id}
    for field in payload.keys():
        if field in inspect(Question).mapper.column_attrs:
            question[field] = payload[field]

    new = Question(**question)
    add_value(new)

    return make_response(jsonify(table2dict(new)), 201)


@QUESTION_BP.route('/question/<int:question_id>', methods = ['GET'])
def get_question(question_id):
    """
    may not be needed but returns a specfic question.
    """
    question = query_question(question_id)
    return_dict = table2dict(question)
    return_dict['answers'] = []
    answers = Answer.query.filter_by(archive=False, question=question_id).all()
    for answer in answers:
        return_dict['answers'].append(table2dict(answer))

    return make_response((jsonify(table2dict(return_dict))), 200)


@QUESTION_BP.route('/question/<int:question_id>', methods = ['PUT'])
def update_question(question_id):
    """
    updates a question, so it should probably send the entire question
    """
    check_token(get_token(request))
    question = question_id(question_id)
    payload = get_payload(request
                          )
    for field in payload.keys():
        if field in inspect(Question).mapper.column_attrs:
            setattr(question, field, payload[field])
    db.session.commit()
    return make_response('', 204)


@QUESTION_BP.route('/question/<int:question_id>', methods = ['DELETE'])
def delete_question(question_id):
    """
    deletes question from a section
    archive
    """
    check_token(get_token(request))
    question = query_question(question_id)
    question.archive = True
    return make_response('', 204)


def query_question(question_id):
    question = Question.query.filter_by(archive=False,
                                        questionid=question_id).first()
    if not question:
        return BadRequest('Question not found')
    return question