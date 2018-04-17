from flask import Flask, jsonify, abort, request, make_response, url_for, Blueprint

QUESTION_BP = Blueprint('question', __name__)

@QUESTION_BP.route('/sections/<int:section_id>/question', methods=['POST'])
def create_question(section_id):
    """
    creates a new question under a section, question id's will probably all be
    unique but, it seems right to specify the section id every time. mongo
    can assign the question id

    {
        "text":"what is this api even doing?",
        "options": [
                    "no one knows",
                    "testing amtgarders",
                    "having a laugh at alex's incompetence",
                    "confusing everyone reading it"],
        "answer": "having a laugh at alex's incompetence"
    }

    """
    message = {}
    message['questoinid'] = 1234
    return make_response(jsonify(message), 201)


@QUESTION_BP.route('/sections/<int:section_id>/question/<int:question_id>', methods = ['GET'])
def get_question(section_id, question_id):
    """
    may not be needed but returns a specfic question.
    return:
        {
        "text":"what is this api even doing?",
        "options": [
                    "no one knows",
                    "testing amtgarders",
                    "having a laugh at alex's incompetence",
                    "confusing everyone reading it"],
        "answer": "having a laugh at alex's incompetence"
    }
    """
    message = {
        "text":"what is this api even doing?",
        "options": [
                    "no one knows",
                    "testing amtgarders",
                    "having a laugh at alex's incompetence",
                    "confusing everyone reading it"],
        "answer": "having a laugh at alex's incompetence"
    }
    return make_response((jsonify(message)), 200)


@QUESTION_BP.route('/sections/<int:section_id>/question/<int:question_id>', methods = ['PUT'])
def update_question(section_id, question_id):
    """
    updates a question, so it should probably send the entire question

    args:
    {
        "text":"what is this api even doing?",
        "options": [
                    "no one knows",
                    "testing amtgarders",
                    "having a laugh at alex's incompetence",
                    "confusing everyone reading it"],
        "answer": "having a laugh at alex's incompetence"
    }
    """
    message = {
        "text": "what is this api even doing?",
        "options": [
            "no one knows",
            "testing amtgarders",
            "having a laugh at alex's incompetence",
            "confusing everyone reading it"],
        "answer": "having a laugh at alex's incompetence"
    }
    return make_response((jsonify(message)), 201)


@QUESTION_BP.route('/sections/<int:section_id>/question/<int:question_id>', methods = ['DELETE'])
def delete_question(section_id, question_id):
    """
    deletes question from a section
    archive
    """
    result = {}
    result['success'] = True
    result['message'] = 'question %s Deleted' % question_id
    return make_response(jsonify(result), 200)
