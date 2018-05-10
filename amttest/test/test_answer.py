"""Test all routes for Answer creation, modification, and query."""

from .base_test import BaseTest

from ..database.tables.answer import Answer


class TestAnswer(BaseTest):
    """Class based on UnitTest.TestCase for testing answer routes."""

    def create_app(self):
        """Configure and stand up the flask app for testing """
        return BaseTest.create_app(self)

    def setUp(self):
        """Create a database for testing."""
        BaseTest.setUp(self)

    def tearDown(self):
        """Delete the database used during testing."""
        BaseTest.tearDown(self)

    def test_get_answer(self):
        """Test the route for querying a single answer."""
        answer1 = Answer(answer='is this an answer?',
                         correct=False,
                         questionid=1)
        self.default_get('amttest/api/answer', answer1)

    def test_add_answer(self):
        """Test the route for creating an answer."""
        payload = {'answer': 'is this an answer?',
                   'correct': False}
        ignore = {'answerid': 235,
                  'chosen': 40,
                  'archive': True}
        self.default_post('amttest/api/question/1/answer',
                          payload,
                          Answer,
                          ignore)

    def test_update_answer(self):
        """Test the route for updating an answer."""
        payload = {'correct': False}
        answer1 = Answer(answer='is this an answer?',
                         correct=False,
                         questionid=1)
        ignore = {'answerid': 235,
                  'chosen': 40,
                  'archive': True}
        self.default_put('amttest/api/answer',
                         payload,
                         answer1,
                         Answer,
                         ignore)

    def test_delete_answer(self):
        """Test the route for deleting (archiving) an answer."""
        answer1 = Answer(answer='is this an answer?',
                         correct=False,
                         questionid=1)
        self.default_delete('amttest/api/answer', answer1)
