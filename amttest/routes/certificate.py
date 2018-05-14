"""Routes that modify the certificate table."""

import logging

from flask import jsonify, request, make_response, Blueprint

from . import get_payload

from ..database.utils import add_value, table2dict
from ..database.tables.answer import Answer
from ..database.tables.certificate import Certificate
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..database.tables.exam import Exam
from ..errors.badrequest import BadRequest
from ..errors.notfound import NotFound
from ..helpers.bphandler import BPHandler
from ..helpers.token import check_token, get_token


CERT_BP = Blueprint('certificate', __name__)
BPHandler.add_blueprint(CERT_BP, url_prefix='/amttest/api')


@CERT_BP.route('/certificate/<int:user_id>/<int:exam_id>', methods=['POST'])
def update_certificate(user_id, exam_id):
    """
    Grade a test and adds the result to the certificate database.

    The payload should be formatted as below
    [
        {questionid: 123,
        answerid:123},
        {questionid:456,
        answerid:456}
    ]

    """
    check_token(get_token(request))
    payload = get_payload(request)

    sections = Section.query.filter_by(archive=False, examid=exam_id).all()
    exam = Exam.query.filter_by(archive=False, examid=exam_id).first()

    if not exam:
        raise NotFound('exam not found')

    needed_questions = 0
    for section in sections:
        needed_questions += section.active_questions

    if needed_questions != len(payload):
        raise BadRequest('submitted exam does not have enough answers')

    cert_dict = {'examid': exam_id,
                 'userid': user_id,
                 'correct': 0,
                 'possible': needed_questions,
                 'passed': False}
    for submission in payload:
        answer = Answer.query.filter_by(archive=False,
                                        answerid=submission[
                                            'answerid'
                                        ]).first()
        question = Question.query.filter_by(archive=False,
                                            questionid=submission[
                                                'questionid'
                                            ]).first()
        if not answer:
            raise BadRequest('no answer found as submitted for question %s'
                             % submission['questionid'])
        if not question:
            raise BadRequest('could not find question %s'
                             % submission['questionid'])

        if answer.correct:
            cert_dict['correct'] += 1
            question.correct += 1
        answer.chosen += 1
        question.used += 1

    if (100.0 * cert_dict['correct'] / cert_dict['possible']) \
            >= exam.pass_percent:
        cert_dict['passed'] = True
    cert = Certificate(**cert_dict)
    # calling this calls commit, which should write all the changes
    # above for stats
    add_value(cert)
    return make_response(jsonify(table2dict(cert)), 201)


@CERT_BP.route('/certificate/<int:user_id>/<int:exam_id>', methods=['GET'])
def get_certificate(user_id, exam_id):
    """Get a specific exam based on the userid and examid."""
    certs = Certificate.query.filter_by(archive=False,
                                        userid=user_id,
                                        examid=exam_id).all()
    cert_dict = []
    for cert in certs:
        tmp = table2dict(cert)
        cert_dict.append(tmp)

    return make_response(jsonify(cert_dict), 200)


@CERT_BP.route('/certificate/user/<int:user_id>', methods=['GET'])
def get_user_certs(user_id):
    """Get all certs for a single user."""
    certs = Certificate.query.filter_by(archive=False, userid=user_id).all()
    cert_dict = []
    for cert in certs:
        tmp = table2dict(cert)
        cert_dict.append(tmp)

    return make_response(jsonify(cert_dict), 200)


@CERT_BP.route('/certificate/exam/<int:exam_id>', methods=['GET'])
def get_test_certs(exam_id):
    """Get all certificates for a given exam id."""
    certs = Certificate.query.filter_by(archive=False, examid=exam_id).all()
    cert_dict = []
    for cert in certs:
        tmp = table2dict(cert)
        cert_dict.append(tmp)

    return make_response(jsonify(cert_dict), 200)


@CERT_BP.route('/certificate', methods=['GET'])
def get_all_certs():
    """Get all certificates int he database."""
    certs = Certificate.query.filter_by(archive=False).all()
    cert_dict = []
    for cert in certs:
        tmp = table2dict(cert)
        cert_dict.append(tmp)

    return make_response(jsonify(cert_dict), 200)
