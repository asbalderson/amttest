from flask import Flask, jsonify, abort, request, make_response, url_for


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

