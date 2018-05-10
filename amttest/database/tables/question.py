"""The question table."""
from .. import DB


class Question(DB.Model):
    """
    questionid: Integer, The unique identifier for the question.
    question: Text, Actual text of the given question.
    sectionid: Integer, Related to the section table. The section that this
        question belongs to
    used: Integer, A count for how many times this question has been asked.
        Plans to use this for statistics.
    correct: Integer, How many times this question has been answered correctly.
    archive: Boolean, When true, will no longer appear in queries.
    """
    __tablename__ = 'question'
    questionid = DB.Column(DB.Integer, nullable=False, primary_key=True)
    question = DB.Column(DB.Text, nullable=False)
    sectionid = DB.Column(DB.Integer, DB.ForeignKey('section.sectionid'),
                          nullable=False)
    archive = DB.Column(DB.Boolean, nullable=False, default=False)
    # these are used potential question analisys
    used = DB.Column(DB.Integer, nullable=False, default=0)
    correct = DB.Column(DB.Integer, nullable=False, default=0)
