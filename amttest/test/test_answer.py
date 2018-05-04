from .base_test import BaseTest

from ..database.tables.answer import Answer
from ..errors import *
from ..routes import answer


class TestAnswer(BaseTest):

    def create_app(self):
        return BaseTest.create_app(self)

    def setUp(self):
        BaseTest.setUp(self)

    def tearDown(self):
        BaseTest.tearDown(self)

    def test_get_answer(self):
        answer = Answer(answer='is this an answer?',
                        correct=False,
                        questionid=1)
        self.default_get('amttest/api/answer', answer)

    def test_add_answer(self):
        payload = {'answer': 'is this an answer?',
                   'correct': False}
        self.default_post('amttest/api/question/1/answer', payload, Answer)

    def test_update_answer(self):
        payload = {'correct': False}
        answer = Answer(answer='is this an answer?',
                        correct=False,
                        questionid=1)
        self.default_put('amttest/api/answer', payload, answer, Answer)

    def test_delete_answer(self):
        answer = Answer(answer='is this an answer?',
                        correct=False,
                        questionid=1)
        self.default_delete('amttest/api/answer', answer)
