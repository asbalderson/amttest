import logging
import json
import random

from flask import jsonify, request, make_response, Blueprint
from pprint import pformat
from sqlalchemy import inspect

from ..errors.badrequest import BadRequest
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

from ..database import db
from ..database.utils import table2dict
from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..database.tables.exam import Exam


EXAM_BP = Blueprint('exam', __name__)
BPHandler.add_blueprint(EXAM_BP, url_prefix='/amttest/api')


@EXAM_BP.route('/exam', methods=['GET'])
def get_examss():
    """
    gets all tests which exists
    :return:
    """
    data = Exam.query.filter_by(archive=False).all()
    return_list = []
    for exam in data:
        return_list.append(table2dict(exam))

    return make_response((jsonify(return_list)), 200)


@EXAM_BP.route('/exam/<int:exam_id>/take', methods = ['GET'])
def get_randomized_exam(exam_id):
    """
    returns a randomized exam with a list of questions based on parameters set
    by the admin on exam creation.
    :param test_id:
    :return:
    """
    logger = logging.getLogger(__name__)
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise BadRequest('exam does not exist')

    exam_dict = table2dict(exam)
    exam_dict['questions'] = []
    sections = Section.query.filter_by(archive=False, examid=exam.examid)
    for section in sections:
        if section.active_questions == 0:
            continue
        all_questions = Question.query.filter_by(archive=False, sectionid=section.sectionid).all()
        used_questions = random.sample(all_questions, section.active_questions)
        for question in used_questions:
            toadd = {'questionid': question.questionid,
                     'question': question.question,
                     'answers': []}
            answers = Answer.query.filter_by(archive=False, questionid=question.questionid).all()
            random.shuffle(answers)
            for answer in answers:
                answer_dict= {'answerid': answer.answerid,
                              'answer': answer.answer}
                toadd['answers'].append(answer_dict)
            exam_dict['questions'].append(toadd)
            random.shuffle(exam_dict['questions'])

    return make_response(jsonify(exam_dict), 200)


@EXAM_BP.route('/exam/<int:exam_id>', methods = ['GET'])
def get_exam(exam_id):
    """
    returns the exam information, and the section names and ids for that exam

    also need to to flag the exam as grabed once before, so it cant be grabbed again
    """
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise BadRequest('exam not found')
    return make_response(jsonify(table2dict(exam)), 200)


@EXAM_BP.route('/exam/', methods = ['POST'])
def create_exam():
    """
    Creates a new exam.
    """
    check_token(get_token(request))
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    tabledata = {}
    for column in payload.keys():
        if column not in inspect(Exam).mapper.column_attrs:
            continue
        else:
            tabledata[column] = payload[column]

    exam = Exam(**tabledata)
    db.session.add(exam)
    db.session.commit()
    db.session.refresh(exam)

    return make_response(jsonify(table2dict(exam)), 201)


@EXAM_BP.route('/exam/<int:exam_id>', methods = ['PUT'])
def update_exam(exam_id):
    """
    updates exam if parameters need to be changed, things like
    name,
    """
    check_token(get_token(request))

    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise BadRequest('exam not found')

    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    for field in payload.keys():
        if field in table2dict(exam).keys():
            setattr(exam, field, payload[field])

    db.session.commit()

    return make_response('', 204)


@EXAM_BP.route('/exam/<int:exam_id>', methods = ['DELETE'])
def delete_exam(exam_id):
    """
    removes a test (archive)
    """
    check_token(get_token(request))
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()
    if not exam:
        raise BadRequest('exam not found')
    exam.archive = True
    db.commit()
    return make_response('', 204)
