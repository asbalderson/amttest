from flask import Flask, jsonify, abort, request, make_response, url_for, Blueprint


sections = [
    {
    'title': u'example_section',
    'section_id': 0,
    },
    {
    'title': u'miscellaneous',
    'section_id': 1,

    }
]

SECTION_BP = Blueprint('sections', __name__)

#i think this is all admin stuff?
@SECTION_BP.route('/sections/str:section_name', methods=['POST'])
def create_section(section_name):
    """
    creates a new section
    """
    message = {}
    message['section_id'] = 1234
    return make_response(jsonify(message), 201)


@SECTION_BP.route('/sections', methods=['GET'])
def get_all_sections():
    """
    gets all the section names and uid's
    return:
    {
        {
            'title': 'Rules of Engagement',
            'uid': 2
        },
        {
            'title': 'Misc',
            'uid': 1
        }
    }
    """
    message =[
        {
            'title': 'Rules of Engagement',
            'section_id': 2
        },

        {
            'title': 'Misc',
            'section_id': 1
        }
    ]
    return make_response(jsonify(message), 200)


@SECTION_BP.route('/sections/<int:section_id>', methods = ['GET'])
def get_section(section_id):
    """
    returns all the section data + questions for a given section,
    actually dont know if this is needed, might be able to just
    get questions for a section id
    """
    message ={
            'title': 'Rules of Engagement',
            'section_id': 2,
            'questoin_ids': [1,2,3,4]
        }
    return make_response(jsonify(message), 200)


@SECTION_BP.route('/sections/<int:section_id>', methods = ['PUT'])
def update_section(section_id):
    """
    this one is probalby not needed either, unless we rename a section
    """
    message ={
            'title': 'Rules of Engagement',
            'section_id': 2
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
    result = {}
    result['success'] = True
    result['message'] = 'section %s Deleted' % section_id
    return make_response(jsonify(result), 200)