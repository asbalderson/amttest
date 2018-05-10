"""Test all routes for Certificate creation, modification, and query."""

import json

from .base_test import BaseTest

from ..database.utils import table2dict
from ..database.tables.answer import Answer
from ..database.tables.certificate import Certificate
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..database.tables.exam import Exam


class TestExam(BaseTest):
    """Class based on UnitTest.TestCase for testing certificate routes."""

    def create_app(self):
        """Configure and stand up the flask app for testing."""
        return BaseTest.create_app(self)

    def setUp(self):
        """Create a database for testing."""
        BaseTest.setUp(self)

    def tearDown(self):
        """Delete the database used during testing."""
        BaseTest.tearDown(self)

    def test_get_all_certs(self):
        """Test the route for getting all certificates."""
        cert = Certificate(userid=1,
                           examid=1,
                           correct=1,
                           possible=1,
                           passed=True)
        cert2 = Certificate(userid=2,
                            examid=1,
                            correct=1,
                            possible=1,
                            passed=True)
        self.default_get_all('amttest/api/certificate', [cert, cert2])

    def test_get_certificate(self):
        """Test the route for getting a single certificate by id."""
        cert = Certificate(userid=1,
                           examid=1,
                           correct=1,
                           possible=1,
                           passed=True)
        cert2 = Certificate(userid=1,
                            examid=1,
                            correct=1,
                            possible=1,
                            passed=True)
        self.default_get_all('amttest/api/certificate/1/1', [cert, cert2])

        no_user_resp = self.client.get('amttest/api/certificate/42/1')
        self.assert200(no_user_resp,
                       'no user should still return an empty list')
        self.assertEqual(no_user_resp.json, [],
                         'if user does not exist, response should return an '
                         'empty list')

    def test_get_user_certs(self):
        """Test the route for getting all of a single users certificate."""
        cert = Certificate(userid=1,
                           examid=1,
                           correct=1,
                           possible=1,
                           passed=True)
        cert2 = Certificate(userid=1,
                            examid=2,
                            correct=1,
                            possible=1,
                            passed=True)
        self.default_get_all('amttest/api/certificate/user/1', [cert, cert2])

    def test_get_test_certs(self):
        """Test the route for getting all certs based on examid."""
        cert = Certificate(userid=1,
                           examid=1,
                           correct=1,
                           possible=1,
                           passed=True)
        cert2 = Certificate(userid=2,
                            examid=1,
                            correct=1,
                            possible=1,
                            passed=True)
        self.default_get_all('amttest/api/certificate/exam/1', [cert, cert2])

    def test_update_certs(self):
        """Test the creation of a new certificate, and exam grading."""
        self.enter_data()
        response_no_header = self.client.post('amttest/api/certificate/1/1')
        self.assert400(response_no_header, 'post should require a token')
        response_no_data = self.client.post('amttest/api/certificate/1/1',
                                            headers=self.header_dict)
        self.assert400(response_no_data,
                       'some data is required for a new entry')

        response_no_exam = self.client.post('amttest/api/certificate/1/42',
                                            headers=self.header_dict,
                                            data=json.dumps(['abc', '123']))
        self.assert400(response_no_exam,
                       'if exam doesnt exist, it cant be graded')

        short_payload = [
            {'questionid': 1,
             'answerid': 3},
            {'questionid': 2,
             'answerid': 5},
            {'questionid': 3,
             'answerid': 12}
        ]
        response_mini_payload = self.client.post('amttest/api/certificate/1/1',
                                                 headers=self.header_dict,
                                                 data=json.dumps(
                                                     short_payload))
        self.assert400(response_mini_payload,
                       'There must be equal answers to active questions from '
                       'each section')

        payload_bad_question = [
            {'questionid': 42,
             'answerid': 3},
            {'questionid': 2,
             'answerid': 5},
            {'questionid': 3,
             'answerid': 12},
            {'questionid': 4,
             'answerid': 13}
        ]

        response_bad_question = self.client.post(
            'amttest/api/certificate/1/1',
            headers=self.header_dict,
            data=json.dumps(payload_bad_question))
        self.assert400(response_bad_question,
                       'if a question is missing, grading should fail')
        payload_bad_answer = [
            {'questionid': 1,
             'answerid': 42},
            {'questionid': 2,
             'answerid': 5},
            {'questionid': 3,
             'answerid': 12},
            {'questionid': 4,
             'answerid': 13}
        ]

        response_bad_answer = self.client.post('amttest/api/certificate/1/1',
                                               headers=self.header_dict,
                                               data=json.dumps(
                                                   payload_bad_answer))
        self.assert400(response_bad_answer,
                       'if an answer is missing, grading should fail')

        payload = [
            {'questionid': 1,
             'answerid': 3},
            {'questionid': 2,
             'answerid': 5},
            {'questionid': 3,
             'answerid': 12},
            {'questionid': 4,
             'answerid': 13}
        ]

        response_correct = self.client.post('amttest/api/certificate/1/1',
                                            headers=self.header_dict,
                                            data=json.dumps(payload))
        self.assertEqual(response_correct.status_code, 201,
                         'grading should return 201')
        self.assertTrue(response_correct.json['passed'],
                        'grading should give a pass with all correct')
        self.assertEqual(response_correct.json['correct'], 4,
                         'all questions should be correct')
        self.assertEqual(response_correct.json['possible'], len(payload),
                         'each question should be graded, all questions are '
                         'the possible score')
        question = Question.query.filter_by(questionid=1).first()
        self.assertEqual(question.correct, 1,
                         'stats should update for getting a question correct')
        self.assertEqual(question.used, 1,
                         'stats should flag a question as being used')
        answer = Answer.query.filter_by(answerid=3).first()
        self.assertEqual(answer.chosen, 1,
                         'stats should update answers for being used')
        cert_pass = Certificate.query.filter_by(
            certid=response_correct.json['certid']).first()
        cert_dict = table2dict(cert_pass)
        cert_dict.pop('testdate')
        self.compare_object(cert_dict, response_correct.json)

        payload_wrong = [
            {'questionid': 1,
             'answerid': 2},
            {'questionid': 2,
             'answerid': 6},
            {'questionid': 3,
             'answerid': 12},
            {'questionid': 4,
             'answerid': 13}
        ]
        response_wrong = self.client.post('amttest/api/certificate/1/1',
                                          headers=self.header_dict,
                                          data=json.dumps(payload_wrong))
        self.assertEqual(response_wrong.status_code, 201,
                         'even wrong answers should return a 201')
        self.assertFalse(response_wrong.json['passed'],
                         'failed tests should fail')

    def enter_data(self):
        """Generate test data for exam testing."""
        data = list()
        data.append(Exam(name='Reeves Test'))
        data.append(Section(name='Rules of Play',
                            examid=1,
                            active_questions=2))
        data.append(Question(
            question='How many magic points does a caster get per level?',
            sectionid=1))
        data.append(Answer(answer='3',
                           correct=False,
                           questionid=1))
        data.append(Answer(answer='4',
                           correct=False,
                           questionid=1))
        data.append(Answer(answer='5',
                           correct=True,
                           questionid=1))
        data.append(Answer(answer='6',
                           correct=False,
                           questionid=1))
        data.append(Question(
            question='How many credits are required for level 4?',
            sectionid=1))
        data.append(Answer(answer='21', correct=True, questionid=2))
        data.append(Answer(answer='25', correct=False, questionid=2))
        data.append(Answer(answer='20', correct=False, questionid=2))
        data.append(Answer(answer='16', correct=False, questionid=2))

        data.append(Section(name='Safety', examid=1, active_questions=2))
        data.append(Question(
            question='When do shots count after a player is hit in the head?',
            sectionid=2))
        data.append(
            Answer(answer='All hits count even if the player is stunned',
                   correct=False, questionid=3))
        data.append(Answer(
            answer='No hits count until the struck player says they are OK',
            correct=False, questionid=3))
        data.append(Answer(
            answer='No hits count and the striking player should remove '
                   'himself from the field',
            correct=False,
            questionid=3))
        data.append(Answer(
            answer='All hits count, given the struck and striking players '
                   'continue play, otherwise combat should be reset to before '
                   'the strike',
            correct=True,
            questionid=3))
        data.append(Question(
            question='When should "Safety" be called?',
            sectionid=2))
        data.append(Answer(
            answer='When there is an injured player, '
                   'or obstruction on the field',
            correct=True,
            questionid=4))
        data.append(
            Answer(answer='Never, "Hold" should be used instead',
                   correct=False,
                   questionid=4))
        data.append(
            Answer(answer='When there is a dispute of the rules',
                   correct=False,
                   questionid=4))
        data.append(Answer(
            answer='When a player feels that the game is unfair '
                   'and wishes to leave',
            correct=False,
            questionid=4))
        self.add_obj_to_db(data)
