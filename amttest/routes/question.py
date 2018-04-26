from flask import jsonify, request, make_response, Blueprint
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

from ..database.tables.question import Question
from ..database.tables.answer import Answer

import json
import logging

QUESTION_BP = Blueprint('question', __name__)
BPHandler.add_blueprint(QUESTION_BP, url_prefix='/amttest/api')

@QUESTION_BP.route('/sections/<int:section_id>/question', methods=['POST'])
def create_question(section_id):
    """
    creates a new question under a section, question id's will probably all be
    unique but, it seems right to specify the section id every time. mongo
    can assign the question id

    {
        "question":"what is this api even doing?",
        "answers": {
                    "no one knows":False,
                    "testing amtgarders":False,
                    "having a laugh at alex's incompetence":True,
                    "confusing everyone reading it":False
                    },
    }

    """
    check_token(get_token(request))
    message = {}
    message['questoinid'] = 1234
    return make_response(jsonify(message), 201)


@QUESTION_BP.route('/question/<int:question_id>', methods = ['GET'])
def get_question(section_id, question_id):
    """
    may not be needed but returns a specfic question.
    return:
        {
        'question_id as int':
            {
            'question': 'what are we doing',
            'answers':
                [
                    {
                        'answer_id': 5,
                        'answer': 'no one knows',
                        'correct': False
                    },
                    {
                        'answer_id': 6,
                        'answer': 'having a laugh at alex\'s expense',
                        'correct': True
                    },
                ]
            }
        }
    """
    message ={
        'question_id as int':
            {
            'question': 'what are we doing',
            'answers':
                [
                    {
                        'answer_id': 5,
                        'answer': 'no one knows',
                        'correct': False
                    },
                    {
                        'answer_id': 6,
                        'answer': 'having a laugh at alex\'s expense',
                        'correct': True
                    },
                ]
            }
        }
    return make_response((jsonify(message)), 200)


@QUESTION_BP.route('/question/<int:question_id>', methods = ['PUT'])
def update_question(question_id):
    """
    updates a question, so it should probably send the entire question

    args:
    {
        "question":"some updated text?",
    }
    """
    check_token(get_token(request))
    message = {
        "question": "some updated text?",
    }
    return make_response((jsonify(message)), 201)


@QUESTION_BP.route('/question/<int:question_id>', methods = ['DELETE'])
def delete_question(section_id, question_id):
    """
    deletes question from a section
    archive
    """
    check_token(get_token(request))
    result = {}
    result['success'] = True
    result['message'] = 'question %s Deleted' % question_id
    return make_response(jsonify(result), 200)


# there is currently no way to update a questions answers
# gota figure out where to put that route