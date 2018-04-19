from .. import db


class Question(db.Model):
    __tablename__ = 'question'
    questionid = db.Column(db.Integer, nullable=False, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    sectionid = db.Column(db.Integer, db.ForeignKey('section.sectionid'),
                          nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)
