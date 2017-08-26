#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()



# be more specific in the error messages
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)



users = [
    {

        'amtname': u'firelord',
        'fbname': u'alex balderson',
        'email': u'ptmmr.black@gmail.com'
        'uid': u'does facebook have this, mongo will generate one'

        certifications = [
            { 
                'name': u'rules of engagement',
                'correct': u'20',
                'testdate': u'8/22/2017',
                'status': u'passed'
            }
            { 
                'name': u'tournament rules',
                'correct': u'20',
                'testdate': u'3/29/2016',
                'status': u'passed'
            }
        ]

    }    
]



sections = [
    {
    'title': u'example_section'
    'uid': 0

        questions = [
        {
            'question': u'Buy groceries',
            'answers': [u'Cheese', u'Pizza', u'Fruit', u'Tylenol'], 
            'correct': u'Cheese'
        },
        {
            'question': u'Buy groceries',
            'answers': [u'Cheese', u'Pizza', u'Fruit', u'Tylenol'], 
            'correct': 'Cheese'
        }

        ]
    }

    {
    'title': u'miscellaneous'
    'uid': 1

        questions = [
        {
            'question': u'howdo',
            'answers': [u'Cheese', u'Pizza', u'Fruit', u'Tylenol'], 
            'correct': u'Cheese'
        },
        {
            'question': u'whendo',
            'answers': [u'Cheese', u'Pizza', u'Fruit', u'Tylenol'], 
            'correct': u'Cheese'
        }

        ]
    }
]


tests = [
    
    {
        'name': u'rules of engagement',
        'passing score': u'75',
        'time limit': u'60m',
        'expires': u'2y',
        'user agreement': 'i agree that this test was taken honestly blah blah...'
        'sections': {
                        u'example_section':2, 
                        u'miscellaneous':1
                    }
    }

    {
        'name': u'rules of engagement',
        'passing score': u'75',
        'time limit': u'60m',
        'expires': u'2y',
        'sections': [u'example_section':2, u'miscellaneous':1]
    }

]


def make_public_task(task):
    """
    master function called by all functions to publish changes to database, should be replaced
    """
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task
    


@app.route('/users/<int:user_id>', methods = ['GET'])

def get_user(user_id):
    """
    gets user data to be parsed and/or displayed on the admin page
    return: literally everything in the users table, see line 21
            but should probably return only the non expired most 
            recent test result for each user.
    """
    user = filter(lambda t: t['id'] == user_id, users)
    return jsonify( { 'user': make_public_task(user[0]) } )


@app.route('/users', methods = ['POST'])
def create_user():
    """
    creates a shell of a user, with their uid, amtname, name, and email
    args:
        {
            "amtname": "example",
            "email": "example@amtgard.com",
            "name": "jane doe",
            "uid": "is this email?"
        }
    """
    user = {
        'amtname': request.json['amtname'],
        'fbname': request.json['fbname']
    }
    users.append(user)
    return jsonify( { 'user': make_public_task(user) } ), 201

@app.route('/users/<int:user_uid>', methods = ['PUT'])
def update_user(user_uid):
    """
    updates user with new information, generally after a user has submitted a test,
    uid is required, whatever information is being updated should be included
    {
        "uid": "whatever this is",
        "email": "jane.doe@example.com",
    }

    """
    if 'username' in request.json and type(request.json['username']) != unicode:
        abort(400)
    if 'passed' in request.json and type(request.json['passed']) is not unicode:
        abort(400)
    user[0]['amtname'] = request.json.get('amtname', user[0]['amtname'])
    user[0]['fbname'] = request.json.get('fbname', user[0]['fbname'])
    # updating certifcations table may be tricky within the user table: may need seperate
    # "update_certificates" method
    #user[0]['certifications'] = request.json.get('certifications', user[0]['certifications'])
    return jsonify( { 'user': make_public_task(user[0]) } )

@app.route('/certificate/<int user_uid>/<int test_id>', methods = ['post'])
def update_certificate(user_uid, test_id):
    """
    adds a new test result to the users certificate.  date can be auto gnerated
    so the only missing information is the users score since pass fail can be
    calculated on the fly and droped in.

    {
        "correct": 3 
    }
    """
    pass


@app.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    """
    removes a user, probably because something went wrong :)
    """
    user = filter(lambda t: t['id'] == user_id, users)
    users.remove(user[0])
    return jsonify( { 'result': True } )


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
    return jsonify( { 'test': make_public_task(test[0]) } )

@app.route('/tests/<int:test_id>', methods = ['DELETE'])
@auth.login_required
def delete_test(test_id):
    """
    removes a test (archive)
    """    
    test = filter(lambda t: t['id'] == test_id, tests)
    tests.remove(test[0])
    return jsonify( { 'result': True } )
 

def submit_test():
    """
    might be a frontend move, but should compare user entered results to
    question answers and provide a score
    """
    pass

def parse_xls(filexls):
    """
    It might be good to have a way to suck in a bunch of questions from a
    spreadsheet or some othe rformat, this is holding for that
    """
    pass

if __name__ == '__main__':
app.run(debug = True)