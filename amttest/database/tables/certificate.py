import datetime

from .. import db

class Certificate(db.Model):
    __tablename__ = 'certificate'
    certid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'),
                    nullable=False)
    testid = db.Column(db.Integer, db.ForeignKey('test.testid'),
                       nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    possible = db.Column(db.Integer, nullable=False)
    testdate = db.Column(db.DateTime, nullable=False,
                      default=datetime.datetime.utcnow)
    passed = db.Column(db.Boolean, nullable=False, default=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)
