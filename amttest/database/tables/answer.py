from .. import db


class Answer(db.Model):
    __tablename__ = 'answer'
    answerid = db.Column(db.Integer, nullable=False, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Boolean, nullable=False, default=False)
    questionid = db.Column(db.Integer, db.ForeignKey('question.questionid'),
                           nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)
