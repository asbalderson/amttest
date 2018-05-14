"""Test all routes for Question creation, modification, and query."""

from .base_test import BaseTest

from ..database import DB
from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section


class TesSection(BaseTest):
    """Class based on UnitTest.TestCase for testing certificate routes."""

    def create_app(self):
        """Configure and stand up the flask app for testing."""
        return BaseTest.create_app(self)

    def setUp(self):
        """Create a database for testing."""
        BaseTest.setUp(self)
        answer = Answer(answer='is this an answer?', correct=False,
                        questionid=1)
        answer2 = Answer(answer='what about this?',
                         correct=False,
                         questionid=1)
        answer3 = Answer(answer='this for sure!', correct=True, questionid=1)
        section = Section(name='just a filler', examid=1)
        self.add_obj_to_db([answer, answer2, answer3, section])

    def tearDown(self):
        """Delete the database used during testing."""
        BaseTest.tearDown(self)

    def test_get_question(self):
        """Test the route for querying a single question."""
        question1 = Question(question='what is not a question?', sectionid=1)
        self.default_get('amttest/api/question', question1, ignore=['answers'])

    def test_add_question(self):
        """Test the route for adding a question."""
        payload = {'question': 'what is this?'}
        ignore = {'archive': True,
                  'correct': 700,
                  'questionid': 21,
                  'used': 98}

        self.default_post('amttest/api/section/1/question',
                          payload,
                          Question,
                          ignore)

    def test_update_question(self):
        """Test the route for updating a question."""
        payload = {'question': 'we changed it'}
        question1 = Question(question='what is not a question?', sectionid=1)
        ignore = {'archive': True,
                  'correct': 700,
                  'questionid': 21,
                  'used': 98}
        self.default_put('amttest/api/question',
                         payload,
                         question1,
                         Question,
                         ignore)

    def test_delete_question(self):
        """Test the route for deleting (archiving) a question."""
        question1 = Question(question='what is not a question?', sectionid=2)
        section = Section(examid=1, name='bacon', active_questions=0)
        self.add_obj_to_db([section])
        self.default_delete('amttest/api/question', question1)

        section.active_questions = 3
        DB.session.commit()

        bad_delete = self.client.delete('amttest/api/question/1')
        self.assert403(bad_delete, 'cannot delete an already deleted question')
