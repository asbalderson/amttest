import logging
import random

from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from . import get_payload

from ..database import db
from ..database.utils import add_value, table2dict
from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..database.tables.exam import Exam
from ..errors.badrequest import BadRequest
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token


EXAM_BP = Blueprint('exam', __name__)
BPHandler.add_blueprint(EXAM_BP, url_prefix='/amttest/api')


@EXAM_BP.route('/exam', methods=['GET'])
def get_exams():
    """
    gets all tests which exists
    :return:
    """
    data = Exam.query.filter_by(archive=False).all()
    return_list = []
    for exam in data:
        return_list.append(table2dict(exam))

    return make_response(jsonify(return_list), 200)


@EXAM_BP.route('/exam/<int:exam_id>/take', methods=['GET'])
def get_randomized_exam(exam_id):
    """
    returns a randomized exam with a list of questions based on parameters set
    by the admin on exam creation.
    :param exam_id:
    :return:
    """
    logger = logging.getLogger(__name__)
    exam = query_exam(exam_id)

    exam_dict = table2dict(exam)
    exam_dict['questions'] = []
    sections = Section.query.filter_by(archive=False, examid=exam.examid)
    for section in sections:
        if section.active_questions == 0:
            continue
        all_questions = Question.query.filter_by(archive=False,
                                                 sectionid=section.sectionid
                                                 ).all()
        used_questions = random.sample(all_questions, section.active_questions)
        for question in used_questions:
            toadd = {'questionid': question.questionid,
                     'question': question.question,
                     'answers': []}
            answers = Answer.query.filter_by(archive=False,
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
    """
    returns the exam information, and the section names and ids for that exam

    also need to to flag the exam as grabed once before, so it cant be
    grabbed again
    """
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise BadRequest('exam not found')
    return make_response(jsonify(table2dict(exam)), 200)


@EXAM_BP.route('/exam', methods=['POST'])
def create_exam():
    """
    Creates a new exam.
    """
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
    """
    updates exam if parameters need to be changed, things like
    name,
    """
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

    db.session.commit()

    return make_response('', 204)


@EXAM_BP.route('/exam/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    """
    removes a test (archive)
    """
    check_token(get_token(request))
    exam = query_exam(exam_id)
    exam.archive = True
    db.session.commit()
    return make_response('', 204)


def query_exam(exam_id):
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise BadRequest('exam not found')
    return exam
