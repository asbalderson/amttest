from .base_test import BaseTest

from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..errors import *
from ..routes import question


class TesSection(BaseTest):

    def create_app(self):
        return BaseTest.create_app(self)


    def setUp(self):
        BaseTest.setUp(self)
        answer = Answer(answer='is this an answer?', correct=False,
                        questionid=1)
        answer2 = Answer(answer='what about this?', correct=False, questionid=1)
        answer3 = Answer(answer='this for sure!', correct=True, questionid=1)
        self.add_obj_to_db([answer, answer2, answer3])


    def tearDown(self):
        BaseTest.tearDown(self)


    def test_get_question(self):
        question = Question(question='what is not a question?', sectionid=1)
        self.default_get('amttest/api/question', question, ignore=['answers'])


    def test_add_question(self):
        payload = {'question': 'what is this?'}
        self.default_post('amttest/api/section/1/question', payload, Question, )


    def test_update_question(self):
        payload = {'question': 'we changed it'}
        question = Question(question='what is not a question?', sectionid=1)
        self.default_put('amttest/api/question', payload, question, Question)


    def test_delete_question(self):
        question = Question(question='what is not a question?', sectionid=1)
        self.default_delete('amttest/api/question', question)
