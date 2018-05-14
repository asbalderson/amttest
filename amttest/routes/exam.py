"""Routes for working with the exam table."""

import logging
import random

from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from . import get_payload

from ..database import DB
from ..database.utils import add_value, table2dict
from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..database.tables.exam import Exam
from ..errors.badrequest import BadRequest
from ..errors.notfound import NotFound
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token


EXAM_BP = Blueprint('exam', __name__)
BPHandler.add_blueprint(EXAM_BP, url_prefix='/amttest/api')


@EXAM_BP.route('/exam', methods=['GET'])
def get_exams():
    """Get all exams which are not archived."""
    data = Exam.query.filter_by(archive=False).all()
    return_list = []
    for exam in data:
        return_list.append(table2dict(exam))

    return make_response(jsonify(return_list), 200)


@EXAM_BP.route('/exam/<int:exam_id>/take', methods=['GET'])
def get_randomized_exam(exam_id):
    """
    Generate a randomized test for a user to take.

    Questions are randomly selected for each section, and answers are scrambled
    by order.  Questions are then scrambled.
    """
    logger = logging.getLogger(__name__)
    exam = query_exam(exam_id)

    exam_dict = table2dict(exam)
    exam_dict['questions'] = []
    sections = Section.query.filter_by(archive=False, examid=exam.examid)
    for section in sections:
        if section.active_questions == 0:
            continue
        all_questions = Question.query.filter_by(
            archive=False,
            sectionid=section.sectionid
        ).all()
        used_questions = random.sample(all_questions, section.active_questions)
        for question in used_questions:
            toadd = {'questionid': question.questionid,
                     'question': question.question,
                     'answers': []}
            answers = Answer.query.filter_by(
                archive=False,
                questionid=question.questionid
            ).all()
            random.shuffle(answers)
            for answer in answers:
                answer_dict = {'answerid': answer.answerid,
                               'answer': answer.answer}
                toadd['answers'].append(answer_dict)
            exam_dict['questions'].append(toadd)
            random.shuffle(exam_dict['questions'])

    return make_response(jsonify(exam_dict), 200)


@EXAM_BP.route('/exam/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    """Get one single exam based on the id."""
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise NotFound('exam not found')
    return make_response(jsonify(table2dict(exam)), 200)


@EXAM_BP.route('/exam', methods=['POST'])
def create_exam():
    """Create a new exam."""
    check_token(get_token(request))
    payload = get_payload(request)
    ignore = ['archive', 'examid']
    tabledata = {}
    for field in payload.keys():
        if field == 'pass_percent':
            if payload[field] > 100 or payload[field] < 1:
                raise BadRequest('pass_percent must be between 1 and 100')

        if field not in inspect(Exam).mapper.column_attrs \
                or field in ignore:
            continue

        tabledata[field] = payload[field]

    exam = Exam(**tabledata)
    add_value(exam)

    return make_response(jsonify(table2dict(exam)), 201)


@EXAM_BP.route('/exam/<int:exam_id>', methods=['PUT'])
def update_exam(exam_id):
    """Update the exam based on the payload supplied."""
    check_token(get_token(request))

    exam = query_exam(exam_id)
    payload = get_payload(request)
    ignore = ['archive', 'examid']
    for field in payload.keys():
        if field in ignore:
            continue

        if field == 'pass_percent':
            if payload[field] > 100 or payload[field] < 1:
                raise BadRequest('pass_percent must be between 1 and 100')

        if field in table2dict(exam).keys():
            setattr(exam, field, payload[field])

    DB.session.commit()

    return make_response('', 204)


@EXAM_BP.route('/exam/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    """Set the archive flag to True, "removing" the test."""
    check_token(get_token(request))
    exam = query_exam(exam_id)
    exam.archive = True
    DB.session.commit()
    return make_response('', 204)


def query_exam(exam_id):
    """Get an exam from the database, or raise a not found."""
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise NotFound('exam not found')
    return exam
