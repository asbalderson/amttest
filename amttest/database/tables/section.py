from .. import db


class Section(db.Model):
    __tablename__ = 'section'
    sectionid = db.Column(db.Integer, primary_key=True, nullable=False)
    section_name = db.Column(db.Text, nullable=False)
    testid = db.Column(db.Integer, db.ForeignKey('test.testid'))
    question_number = db.Column(db.Integer, default=0)
    archive = db.Column(db.Boolean, nullable=False, default=False)
