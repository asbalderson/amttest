from collections import defaultdict
from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

import logging
import json

from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

from ..database import db
from ..database.tables.answer import Answer
from ..database.tables.section import Section
from ..database.tables.question import Question
from ..database.utils import table2dict

from ..errors.badrequest import BadRequest

sections = [
    {
    'name': u'example_section',
    'section_id': 0,
    'active_qestions': 10
    },
    {
    'name': u'miscellaneous',
    'section_id': 1,
    'active_qestions': 5
    }
]

SECTION_BP = Blueprint('sections', __name__)
BPHandler.add_blueprint(SECTION_BP, url_prefix='/amttest/api')


@SECTION_BP.route('/tests/<int:test_id>/sections', methods=['POST'])
def create_section(test_id):
    """
    creates a new section
    """
    check_token(get_token(request))
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    fields = {'testid':test_id}
    for column in payload.keys():
        if column not in inspect(Section).mapper.column_attrs:
            continue
        fields[column] = payload[column]
    section = Section(**fields)
    db.session.add(section)
    db.session.commit()
    db.session.refresh(section)

    return make_response(jsonify(table2dict(section)), 201)


@SECTION_BP.route('/tests/<int:test_id>/sections', methods=['GET'])
def get_test_sections(test_id):
    section_data = Section.query.filter_by(archive=False, testid=test_id).all()

    section_list = []
    for section in section_data:
        section.append(table2dict(section))

    return make_response(jsonify(section_list), 200)


@SECTION_BP.route('/sections', methods=['GET'])
def get_all_sections():
    """
    gets all the section names and uid's
    return:
    {
    'section_name': u'example_section',
    'section_id': 0,
    'active_qestions': 10
    },
    {
    'section_name': u'miscellaneous',
    'section_id': 1,
    'active_qestions': 5
    }
    """
    section_data = Section.query.filter_by(archive=False).all()

    section_list = []
    for section in section_data:
        section.append(table2dict(section))

    return make_response(jsonify(section_list), 200)


@SECTION_BP.route('/sections/<int:section_id>', methods = ['GET'])
def get_section(section_id):
    """
    returns all the section data + questions for a given section,
    actually dont know if this is needed, might be able to just
    get questions for a section id
    """

    section = Section.query.filter_by(archive=False, sectionid=section_id).first()
    if not section:
        raise BadRequest('Section does not exist')

    return_dict = table2dict(section)

    questions = Question.query.filter_by(archive=False, sectionid=section.sectionid)
    return_dict['questions'] = []
    for question in questions:
        question_dict = table2dict(question)
        question_dict['answers'] = []
        answers = Answer.query.filter_by(archive=False, questionid=question.questionid)
        for answer in answers:
            question_dict['answers'].append(table2dict(answer))
        return_dict['questions'].append(question_dict)

    return make_response(jsonify(return_dict), 200)


@SECTION_BP.route('/sections/<int:section_id>', methods = ['PUT'])
def update_section(section_id):
    """
    this is used to change the number of questions usd for a section
    """
    check_token(get_token(request))
    payload_raw = request.data.decode()
    payload = json.loads(payload_raw)
    section = Section.query.filter_by(archive=False, sectionid=section_id).first()
    if not section:
        raise BadRequest('Section not found')

    for field in payload.keys():
        if field in inspect(Section).mapper.column_attrs:
            setattr(section, field, payload[field])

    db.session.commit()

    return make_response('', 204)

@SECTION_BP.route('/sections/<int:section_id>', methods = ['DELETE'])
def delete_section(section_id):
    """
    removes a section, tests calling removed section will be invalid
    should produce error if section is in use
    """
    check_token(get_token(request))
    section = Section.query.filter_by(archive=False, sectionid=section_id).first()
    section.archive = False
    db.session.commit()
    return make_response('', 204)