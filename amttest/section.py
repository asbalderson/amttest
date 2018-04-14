from flask import Flask, jsonify, abort, request, make_response, url_for

@app.route('/sections/str:section_name', methods=['POST'])
def create_section(section_name):
    """
    creates a new section
    """
    pass


@app.route('/sections', methods=['GET'])
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
    pass

@app.route('/sections/<int:section_id>', methods = ['GET'])
def get_section(section_id):
    """
    returns all the section data + questions for a given section,
    actually dont know if this is needed, might be able to just
    get questions for a section id
    """
    section = filter(lambda t: t['id'] == section_id, sections)
    return jsonify( { 'section': make_public_task(section[0]) } )


@app.route('/sections/<int:section_id>', methods = ['PUT'])
def update_section(section_id):
    """
    this one is probalby not needed either, unless we rename a section
    """
    section = filter(lambda t: t['id'] == section_id, sections)

    section[0]['title'] = request.json.get('title', section[0]['title'])
    return jsonify( { 'section': make_public_task(section[0]) } )


@app.route('/sections/<int:section_id>', methods = ['DELETE'])
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
    section = filter(lambda t: t['id'] == section_id, sections)
    sections.remove(section[0])
    return jsonify( { 'result': True } )


@app.route('/sections/<int: section_id>/questoin' methods=['POST'])
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
    pass

# could also have /sections/<int:section_id>/questions/<int:question_id>
@app.route('/sections/<int section_id>/questions/<int:question_id>', methods = ['GET'])
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
    question = filter(lambda t: t['id'] == question_id, questions)
    return jsonify( { 'question': make_public_task(question[0]) } )

@app.route('/sections/<int section_id>/questions/<int:question_id>', methods = ['PUT'])
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
    question = filter(lambda t: t['id'] == question_id, questions)

    # needs to access questions table, dont know how this would be implemented
    question[0]['question'] = request.json.get('question', question[0]['question'])
    return jsonify( { 'question': make_public_task(question[0]) } )

@app.route('/sections/<int section_id>/questions</int:question_id>', methods = ['DELETE'])
def delete_question(section_id, question_id):
    """
    deletes question from a section
    """
    question = filter(lambda t: t['id'] == question_id, questions)
    questions.remove(question[0])
    return jsonify( { 'result': True } )
