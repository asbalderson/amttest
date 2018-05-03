import json

from .base_test import BaseTest

from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..errors import *
from ..routes import section


class TestSection(BaseTest):

    def create_app(self):
        return BaseTest.create_app(self)


    def setUp(self):
        BaseTest.setUp(self)
        answer = Answer(answer='is this an answer?', correct=False,
                        questionid=1)
        answer2 = Answer(answer='what about this?', correct=False, questionid=1)
        answer3 = Answer(answer='this for sure!', correct=True, questionid=1)
        question = Question(question='what is not a question?', sectionid=1)
        self.add_obj_to_db([answer, answer2, answer3, question])


    def tearDown(self):
        BaseTest.tearDown(self)


    def test_get_all_sections(self):
        section1 = Section(name='world of unknown',
                           examid=1)
        section2 = Section(name='world of known',
                           examid=1)

        self.default_get_all('amttest/api/section', [section1, section2])


    def test_get_section(self):
        section1 = Section(name='world of unknown',
                           examid=1)
        self.default_get('amttest/api/section', section1, ignore=['questions'])


    def test_get_exam_sections(self):
        section1 = Section(name='world of unknown',
                           examid=1)
        section2 = Section(name='world of known',
                           examid=1)
        self.default_get_all('amttest/api/exam/1/section', [section1, section2])


    def test_new_section(self):
        payload = {'name': 'just some section'}
        self.default_post('amttest/api/exam/1/section', payload, Section)


    def test_update_section(self):
        payload = {'name': 'some new section name'}
        section1 = Section(name='world of unknown',
                           examid=1)
        self.default_put('amttest/api/section', payload, section1, Section)

        payload_active_question = {'active_questions': 300}
        result_not_enough_questions = self.client.put('amttest/api/section/1', headers=self.header_dict, data=json.dumps(payload_active_question))
        self.assert400(result_not_enough_questions, 'should not be able to have more active quesitons than questions')


    def test_delete_section(self):
        section1 = Section(name='world of unknown',
                           examid=1)
        self.default_delete('amttest/api/section', section1)
