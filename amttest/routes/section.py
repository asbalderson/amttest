"""Routes that modify the section table."""

import logging

from flask import jsonify, request, make_response, Blueprint
from sqlalchemy import inspect

from . import get_payload

from ..database import DB
from ..database.tables.answer import Answer
from ..database.tables.section import Section
from ..database.tables.question import Question
from ..database.utils import add_value, table2dict
from ..errors.badrequest import BadRequest
from ..errors.notfound import NotFound
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token


SECTION_BP = Blueprint('section', __name__)
BPHandler.add_blueprint(SECTION_BP)


@SECTION_BP.route('/exam/<int:exam_id>/section', methods=['POST'])
def create_section(exam_id):
    """Create a new section."""
    check_token(get_token(request))
    payload = get_payload(request)
    fields = {'examid': exam_id}
    ignore = ['archive', 'sectionid']
    for field in payload.keys():
        if field in ignore:
            continue
        if field not in inspect(Section).mapper.column_attrs:
            continue
        fields[field] = payload[field]
    section = Section(**fields)
    add_value(section)

    return make_response(jsonify(table2dict(section)), 201)


@SECTION_BP.route('/exam/<int:exam_id>/section', methods=['GET'])
def get_exam_sections(exam_id):
    """Get all sections for one exam."""
    section_data = Section.query.filter_by(archive=False, examid=exam_id).all()

    section_list = []
    for section in section_data:
        section_list.append(table2dict(section))

    return make_response(jsonify(section_list), 200)


@SECTION_BP.route('/section', methods=['GET'])
def get_all_sections():
    """Get all sections in the database."""
    section_data = Section.query.filter_by(archive=False).all()

    section_list = []
    for section in section_data:
        section_list.append(table2dict(section))

    return make_response(jsonify(section_list), 200)


@SECTION_BP.route('/section/<int:section_id>', methods=['GET'])
def get_section(section_id):
    """Get one section based on the section id."""
    section = query_section(section_id)
    return_dict = table2dict(section)

    questions = Question.query.filter_by(archive=False,
                                         sectionid=section.sectionid).all()
    return_dict['questions'] = []
    for question in questions:
        question_dict = table2dict(question)
        question_dict['answers'] = []
        answers = Answer.query.filter_by(archive=False,
                                         questionid=question.questionid).all()
        for answer in answers:
            question_dict['answers'].append(table2dict(answer))
        return_dict['questions'].append(question_dict)

    return make_response(jsonify(return_dict), 200)


@SECTION_BP.route('/section/<int:section_id>', methods=['PUT'])
def update_section(section_id):
    """Update a single section based on a payload."""
    check_token(get_token(request))
    payload = get_payload(request)
    section = query_section(section_id)
    ignore = ['archive', 'sectionid']
    for field in payload.keys():
        if field in ignore:
            continue
        if field == 'active_questions':
            questions = Question.query.filter_by(archive=False,
                                                 sectionid=section_id).all()
            if len(questions) < payload['active_questions']:
                raise BadRequest('Cannot have fewer questions than '
                                 'active questions, add some questions first')
        if field in inspect(Section).mapper.column_attrs:
            setattr(section, field, payload[field])

    DB.session.commit()

    return make_response('', 204)


@SECTION_BP.route('/section/<int:section_id>', methods=['DELETE'])
def delete_section(section_id):
    """Set a sections archive flag to True, removing it from all queries."""
    check_token(get_token(request))
    section = query_section(section_id)
    section.archive = True
    DB.session.commit()
    return make_response('', 204)


def query_section(section_id):
    """Query a single section or raise a BadRequest if not found."""
    section = Section.query.filter_by(archive=False,
                                      sectionid=section_id).first()
    if not section:
        raise NotFound('Section not found')
    return section
