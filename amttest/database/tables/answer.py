"""The answer table."""
from .. import DB


class Answer(DB.Model):
    """
    answerid: Integer, Unique identifier for an answer.
    correct: Boolean, True for the correct answer
    questionid: Integer, Relates to the question table. The question this
        answer belongs to.
    archive: Boolean, When true, this question will no longer appear in
        queries.
    chosen: Integer, The number of times this answer has been chosen by a user.
    """
    __tablename__ = 'answer'
    answerid = DB.Column(DB.Integer, nullable=False, primary_key=True)
    answer = DB.Column(DB.Text, nullable=False)
    correct = DB.Column(DB.Boolean, nullable=False, default=False)
    questionid = DB.Column(DB.Integer, DB.ForeignKey('question.questionid'),
                           nullable=False)
    archive = DB.Column(DB.Boolean, nullable=False, default=False)
    chosen = DB.Column(DB.Integer, nullable=False, default=0)
