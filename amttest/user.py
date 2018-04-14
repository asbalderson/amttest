from flask import Flask, jsonify, abort, request, make_response, url_for

from .amttest import AMT_TEST

@AMT_TEST.route('/users/<int:user_id>', methods = ['GET'])
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
        'fbname': reqtuest.json['fbname']
    }
    users.append(user)
    return jsonify( { 'user': make_public_task(user) } ), 201

@app.route('/users/<int:user_uid>', methods = ['PUT'])
def put_update_user(user_uid):
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

@app.route('/users/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    """
    removes a user, probably because something went wrong :)
    """
    user = filter(lambda t: t['id'] == user_id, users)
    users.remove(user[0])
    return jsonify( { 'result': True } )
