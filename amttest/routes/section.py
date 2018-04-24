from flask import jsonify, request, make_response, Blueprint
from ..helpers.bphandler import BPHandler
from ..helpers.token import get_token, check_token

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

#i think this is all admin stuff?
@SECTION_BP.route('/tests/<int:test_id>/section/', methods=['POST'])
def create_section(test_id):
    """
    creates a new section
    """
    check_token(get_token(request))
    message = {}
    message['section_id'] = 1234
    return make_response(jsonify(message), 201)


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
    global sections
    return make_response(jsonify(sections), 200)


@SECTION_BP.route('/sections/<int:section_id>', methods = ['GET'])
def get_section(section_id):
    """
    returns all the section data + questions for a given section,
    actually dont know if this is needed, might be able to just
    get questions for a section id
    """
    message ={
            'name': 'Rules of Engagement',
            'section_id': 2,
            'active_questions': 5,
            'questions': [
                {
                    'question_id as int':{
                        'question': 'what are we doing',
                        'answers':[
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
            ]
        }
    return make_response(jsonify(message), 200)


@SECTION_BP.route('/sections/<int:section_id>', methods = ['PUT'])
def update_section(section_id):
    """
    this is used to change the number of questions usd for a section
    """
    check_token(get_token(request))
    message ={
            'name': 'Rules of Engagement',
            'section_id': 2,
            'active_questions': 5
        }
    return make_response(jsonify(message), 201)

@SECTION_BP.route('/sections/<int:section_id>', methods = ['DELETE'])
def delete_section(section_id):
    """
    removes a section, tests calling removed section will be invalid
    should produce error if section is in use
    AKA there is a new GMR.  deleted sections will be archived,
    so either moved to a new database, or set with an archive flag
    eventually we will need a way to query the archive, but i bet
    i could mirror most of the calls and add a /archive/ infront of
    everything
    """
    check_token(get_token(request))
    result = {}
    result['success'] = True
    result['message'] = 'section %s Deleted' % section_id
    return make_response(jsonify(result), 200)