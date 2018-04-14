from flask import Flask, jsonify, abort, request, make_response, url_for

@app.route('/tests/<int:test_id>', methods = ['GET'])
def get_test(test_id):
    """
    returns the test information, including all the sections, question counts
    form each section, time limits, etc.

    """
    test = filter(lambda t: t['id'] == test_id, tests)
    return jsonify( { 'test': make_public_task(test[0]) } )

@app.route('/tests/<str test_name>', methods = ['POST'])
def create_test(test_name):
    """
    creates a test which can be taken by users, questions will be
    random from a given sections (and probably in a random order too) and
    answers will also come in a random order.  the formatting on this is the
    key to the whole project
    """
    test = {
        'name': request.json['name'],
        'time_limit': request.json['time_limit'],
        'expires': request.json['expires'],
        'passing_score': request.json.get('passing_score', ""),
        'sections': request.json['sections']
    }
    tests.append(test)
    return jsonify( { 'test': make_public_task(test) } ), 201

@app.route('/tests/<int:test_id>', methods = ['PUT'])
def update_test(test_id):
     """
    updates test if parameters need to be changed, things like
    name, sections it takes questions from, number of questions in a section
    time limit, passing score, etc
    {
        "title": "ROP",
        "sections": {
                <section_id>:<questions from that section for the test>
        }
        "timelimit": 60
    }
    """
    test = filter(lambda t: t['id'] == test_id, tests)

    test[0]['name'] = request.json.get('name', test[0]['name'])
    test[0]['time_limit'] = request.json.get('time_lmit', test[0]['time_limit'])
    test[0]['expires'] = request.json.get('expires', test[0]['expires'])
    test[0]['passing_score'] = request.json.get('passing_score', test[0]['passing_score'])
    test[0]['sections'] = request.json.get('sections', test[0]['sections'])
    return jsonify( { 'test': make_public_task(test[0]) } ))

@app.route('/tests/<int:test_id>', methods = ['DELETE'])
@auth.login_required
def delete_test(test_id):
    """
    removes a test (archive)
    """
    test = filter(lambda t: t['id'] == test_id, tests)
    tests.remove(test[0])
    return jsonify( { 'result': True } )
