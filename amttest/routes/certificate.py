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
from ..database.tables.user import User
from ..errors.badrequest import BadRequest
from ..errors.internalservererror import InternalServerError
from ..errors.notfound import NotFound
from ..helpers.bphandler import BPHandler
from ..helpers.token import check_token, get_token


CERT_BP = Blueprint('certificate', __name__)
BPHandler.add_blueprint(CERT_BP)


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
        if submission['answerid'] > 0:

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

    # here we are getting all certs, and then grabbing the one we care about
    cert_list = query_certs(userid=user_id, examid=exam_id)

    for a_cert in cert_list:
        if a_cert['certid'] == cert.certid:
            return make_response(jsonify(table2dict(cert)), 201)

    raise InternalServerError('There should be no way to get here. '
                              'After grading a test, the cert should exist and'
                              'be returned.')


@CERT_BP.route('/certificate/<int:user_id>/<int:exam_id>', methods=['GET'])
def get_certificate(user_id, exam_id):
    """Get a specific exam based on the userid and examid."""
    cert_list = query_certs(userid=user_id, examid=exam_id)

    return make_response(jsonify(cert_list), 200)


@CERT_BP.route('/certificate/user/<int:user_id>', methods=['GET'])
def get_user_certs(user_id):
    """Get all certs for a single user."""
    cert_list = query_certs(userid=user_id)

    return make_response(jsonify(cert_list), 200)


@CERT_BP.route('/certificate/exam/<int:exam_id>', methods=['GET'])
def get_test_certs(exam_id):
    """Get all certificates for a given exam id."""
    cert_list = query_certs(examid=exam_id)

    return make_response(jsonify(cert_list), 200)


@CERT_BP.route('/certificate', methods=['GET'])
def get_all_certs():
    """Get all certificates int he database."""
    cert_list = query_certs()

    return make_response(jsonify(cert_list), 200)


def query_certs(userid=None, examid=None):
    """
    Get all certs with joined values from user and exam tables.

    :param userid: int, Foreign key for a user.
    :param examid: int, Foreign key for an exam.
    :return: list, Dictionaries containing certificate data.
    """
    filter_dict = {'archive': False}

    if userid:
        filter_dict['userid'] = userid
    if examid:
        filter_dict['examid'] = examid

    certs = Certificate.query.with_entities(
        Certificate.certid,
        Certificate.correct,
        Certificate.possible,
        Certificate.passed,
        Certificate.testdate,
        Certificate.examid,
        User.name.label('username'),
        Exam.name.label('examname')
    ).filter_by(
        **filter_dict
    ).join(
        Exam
    ).join(
        User
    ).all()

    cert_list = []
    print(len(certs))
    for cert in certs:
        temp = {
            'certid': cert.certid,
            'correct': cert.correct,
            'possible': cert.possible,
            'passed': cert.passed,
            'testdate': cert.testdate,
            'examid': cert.examid,
            'username': cert.username,
            'examname': cert.examname
        }
        cert_list.append(temp)
    print(cert_list)
    return cert_list
