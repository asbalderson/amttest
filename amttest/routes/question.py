"""Routes which modify the question table."""
import logging

from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from . import get_payload

from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token
from ..database import DB
from ..database.utils import add_value, table2dict
from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..errors.badrequest import BadRequest


QUESTION_BP = Blueprint('question', __name__)
BPHandler.add_blueprint(QUESTION_BP, url_prefix='/amttest/api')


@QUESTION_BP.route('/section/<int:section_id>/question', methods=['POST'])
def create_question(section_id):
    """Create a new question based on a sectionid."""
    check_token(get_token(request))
    payload = get_payload(request)
    question = {'sectionid': section_id}
    ignore = ['archive', 'correct', 'questionid', 'used']
    for field in payload.keys():
        if field in ignore:
            continue
        if field in inspect(Question).mapper.column_attrs:
            question[field] = payload[field]

    new = Question(**question)
    add_value(new)

    return make_response(jsonify(table2dict(new)), 201)


@QUESTION_BP.route('/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Get a single question based on its id. """
    question = query_question(question_id)
    return_dict = table2dict(question)
    return_dict['answers'] = []
    answers = Answer.query.filter_by(archive=False,
                                     questionid=question_id).all()
    for answer in answers:
        return_dict['answers'].append(table2dict(answer))

    return make_response(jsonify(return_dict), 200)


@QUESTION_BP.route('/question/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """Update an existing question."""
    check_token(get_token(request))
    question = query_question(question_id)
    payload = get_payload(request)
    ignore = ['archive', 'correct', 'questionid', 'used']
    for field in payload.keys():
        if field in ignore:
            continue
        if field in inspect(Question).mapper.column_attrs:
            setattr(question, field, payload[field])
    DB.session.commit()
    return make_response('', 204)


@QUESTION_BP.route('/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Set a questions archive flag to True, removing it from queries."""
    check_token(get_token(request))
    question = query_question(question_id)
    section = Section.query.filter_by(archive=False,
                                      sectionid=question.sectionid).first()
    all_question = Question.query.filter_by(archive=False,
                                            sectionid=section.sectionid).all()
    if section.active_questions > len(all_question) - 1:
        raise BadRequest('Archiving question will leave not enough questions '
                         'to meet the requirements for the section.')
    question.archive = True
    DB.session.commit()
    return make_response('', 204)


def query_question(question_id):
    """
    Get a single question, or raise a BadRequest if not found.

    :param question_id: int, primary key for a question.
    :return: Table data for a question.
    """
    question = Question.query.filter_by(archive=False,
                                        questionid=question_id).first()
    if not question:
        raise BadRequest('Question not found')
    return question
