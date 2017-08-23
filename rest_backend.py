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
        'fbname': u'alex balderson'

        certifications = [
            { 
                'name': u'rules of engagement',
                'score': u'75',
                'testdate': u'8/22/2017',
                'status': u'passed'
            }
            { 
                'name': u'tournament rules',
                'score': u'95',
                'testdate': u'3/29/2016',
                'status': u'passed'
            }
        ]

    }

    
]



sections = [
    

    {
    'title': u'example_section'

        questions = [
        {
            'question': u'Buy groceries',
            'answers': u'[Cheese, Pizza, Fruit, Tylenol]', 
            'correct': 'Cheese'
        },
        {
            'question': u'Buy groceries',
            'answers': u'[Cheese, Pizza, Fruit, Tylenol]', 
            'correct': 'Cheese'
        }

        ]
    }

    {
    'title': u'miscellaneous'

        questions = [
        {
            'question': u'howdo',
            'answers': u'[Cheese, Pizza, Fruit, Tylenol]', 
            'correct': 'Cheese'
        },
        {
            'question': u'whendo',
            'answers': u'[Cheese, Pizza, Fruit, Tylenol]', 
            'correct': 'Cheese'
        }

        ]
    }
]


tests = [
    
    {
        'name': u'rules of engagement',
        'passing score': u'75',
        'time limit': u'60m',
        'expires': u '2y',
        'sections': u'['example_section':'2', 'miscellaneous':'1']'

    }

    {
        'name': u'rules of engagement',
        'passing score': u'75',
        'time limit': u'60m',
        'expires': u '2y',
        'sections': u'['example_section':'2', 'miscellaneous':'1']'

    }

]


#comment the functions to say what they are supposed to do, and include an example of data (what it expects to see, or what it is going to send)
#add question functions

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
@auth.login_required
def get_user(user_id):
    """
    gets user data to be parsed and/or displayed on the admin page
    """
    user = filter(lambda t: t['id'] == user_id, users)
    return jsonify( { 'user': make_public_task(user[0]) } )


@app.route('/users', methods = ['POST'])
@auth.login_required
def create_user():
    """
    initializes user upon login, will eventually be replaced with Facebook API
    that will do the initialization and posting
    """
    user = {
        'amtname': request.json['amtname'],
        'fbname': request.json['fbname']
    }
    users.append(user)
    return jsonify( { 'user': make_public_task(user) } ), 201

@app.route('/users/<int:user_id>', methods = ['PUT'])
@auth.login_required
def update_user(user_id):
    """
    updates user with new information, generally after a user has submitted a test
    """
    if 'username' in request.json and type(request.json['username']) != unicode:
        abort(400)
    if 'passed' in request.json and type(request.json['passed']) is not unicode:
        abort(400)
    user[0]['amtname'] = request.json.get('amtname', user[0]['amtname'])
    user[0]['fbname'] = request.json.get('fbname', user[0]['fbname'])
    # updating certifcations table may be tricky within the user table: may need seperate
    # "update_certificates" method
    user[0]['certifications'] = request.json.get('certifications', user[0]['certifications'])
    return jsonify( { 'user': make_public_task(user[0]) } )

@app.route('/users/<int:user_id>', methods = ['DELETE'])
@auth.login_required
def delete_user(user_id):
    """
    removes a user, usually for expired or empty certifications
    """
    user = filter(lambda t: t['id'] == user_id, users)
    users.remove(user[0])
    return jsonify( { 'result': True } )

# could also have /sections/<int:section_id>/questions/<int:question_id>

@app.route('/sections/questions/<int:question_id>', methods = ['GET'])
@auth.login_required
def get_question(question_id):
    """
    supplements get_section call and is used for generating
    a question or viewing question contents
    """
    question = filter(lambda t: t['id'] == question_id, questions)
    return jsonify( { 'question': make_public_task(question[0]) } )

@app.route('/sections/questions/<int:question_id>', methods = ['PUT'])
@auth.login_required
def update_question(question_id):
    """
    updates and/or creates a new question
    """
    question = filter(lambda t: t['id'] == question_id, questions)
    
    # needs to access questions table, dont know how this would be implemented
    question[0]['question'] = request.json.get('question', question[0]['question'])
    return jsonify( { 'question': make_public_task(question[0]) } )
 
@app.route('/sections/questions</int:question_id>', methods = ['DELETE'])
@auth.login_required
def delete_question(question_id):
    """
    deletes question
    """    
    question = filter(lambda t: t['id'] == question_id, questions)
    questions.remove(question[0])
    return jsonify( { 'result': True } )   


@app.route('/sections/<int:section_id>', methods = ['GET'])
@auth.login_required
def get_section(section_id):
    """
    gets section data including questions, most likely to be used by the 
    "get_test" "create_test" and "update_test" methods
    """
    section = filter(lambda t: t['id'] == section_id, sections)
    return jsonify( { 'section': make_public_task(section[0]) } )

@app.route('/sections', methods = ['POST'])
@auth.login_required
def create_section():
    """
    initializes a section with a datastructure and name
    """
    section = {
        'title': request.json['title'],
    }
    sections.append(section)
    return jsonify( { 'section': make_public_task(section) } ), 201

@app.route('/sections/<int:section_id>', methods = ['PUT'])
@auth.login_required
def update_section(section_id):
    """
    updates sections with new information, usually called when
    adding or removing questions
    """
    section = filter(lambda t: t['id'] == section_id, sections)
    
    section[0]['title'] = request.json.get('title', section[0]['title'])
    return jsonify( { 'section': make_public_task(section[0]) } )
    

@app.route('/sections/<int:section_id>', methods = ['DELETE'])
@auth.login_required
def delete_section(section_id):
    """
    removes a section, tests calling removed section will be invalid
    should produce error if section is in use
    """    
    section = filter(lambda t: t['id'] == section_id, sections)
    sections.remove(section[0])
    return jsonify( { 'result': True } )

#come up with a better way to remove a question
#@app.route(/section/<sectionid>/<questionid>)


@app.route('/tests/<int:test_id>', methods = ['GET'])
@auth.login_required
def get_test(test_id):
    """
    gets test data including questions and sections
    called to give user a test or for the admin to view data
    """
    test = filter(lambda t: t['id'] == test_id, tests)
    return jsonify( { 'test': make_public_task(test[0]) } )

@app.route('/tests', methods = ['POST'])
@auth.login_required
def create_test():
    """
    creates a test which can be taken by users
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
@auth.login_required
def update_test(test_id):
     """
    updates test if parameters need to be changed
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
    removes a test
    """    
    test = filter(lambda t: t['id'] == test_id, tests)
    tests.remove(test[0])
    return jsonify( { 'result': True } )
 

def submit_test():
    """
    might be a frontend move, but should compare user entered results to
    question answers and provide a score
    """

def parse_xls(file.xls):
    """
    take external file, parse it, and update section
    with the variables provided
    """

if __name__ == '__main__':
app.run(debug = True)