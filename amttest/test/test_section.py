"""Module for testing routes for section creation, modification and query"""

import json

from .base_test import BaseTest

from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section


class TestSection(BaseTest):
    """ Class based on UnitTest.TestCase for testing section routes."""

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
        question = Question(question='what is not a question?', sectionid=1)
        self.add_obj_to_db([answer, answer2, answer3, question])

    def tearDown(self):
        """Delete the database used during testing."""

        BaseTest.tearDown(self)

    def test_get_all_sections(self):
        """Test the route for querying all section."""
        section1 = Section(name='world of unknown',
                           examid=1)
        section2 = Section(name='world of known',
                           examid=1)

        self.default_get_all('amttest/api/section', [section1, section2])

    def test_get_section(self):
        """Test the route for getting a single section."""
        section1 = Section(name='world of unknown',
                           examid=1)
        self.default_get('amttest/api/section', section1, ignore=['questions'])

    def test_get_exam_sections(self):
        """Test the route for getting all sections for an exam."""
        section1 = Section(name='world of unknown',
                           examid=1)
        section2 = Section(name='world of known',
                           examid=1)
        self.default_get_all('amttest/api/exam/1/section',
                             [section1, section2])

    def test_new_section(self):
        """Test the route for creating a new section."""
        payload = {'name': 'just some section'}
        ignore = {'archive': True,
                  'sectionid': 69}
        self.default_post('amttest/api/exam/1/section',
                          payload,
                          Section,
                          ignore)

    def test_update_section(self):
        """Test the route for updating an existing section."""
        payload = {'name': 'some new section name'}
        ignore = {'archive': True,
                  'sectionid': 69}
        section1 = Section(name='world of unknown',
                           examid=1)
        self.default_put('amttest/api/section',
                         payload,
                         section1,
                         Section,
                         ignore)

        payload_question = {'active_questions': 300}
        missing_questions = self.client.put('amttest/api/section/1',
                                            headers=self.header_dict,
                                            data=json.dumps(payload_question))
        self.assert400(missing_questions,
                       'should not be able to have more active quesitons '
                       'than questions')

    def test_delete_section(self):
        """Test the route for deleting (archiving) a section."""
        section1 = Section(name='world of unknown',
                           examid=1)
        self.default_delete('amttest/api/section', section1)
