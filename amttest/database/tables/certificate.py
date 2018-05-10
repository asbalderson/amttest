"""The certificate table."""
import datetime

from .. import DB


class Certificate(DB.Model):
    """
    Certificate table.

    certid: Integer, The unique identifier for a certificate.
    userid: Integer, Related to the User table. The user this certificate
        belongs to.
    examid: Integer, Related to the Exam table. The exam this certificate
        belongs to.
    correct: Integer, Number of questions that were answered correctly.
    possible: Integer, Number of questions that were given for the exam.
    passed: Boolean, True if the correct/possible was greater than or equal to
        the required passing score from the exam AT THE TIME OF TAKING THE
        TEST.
    testdate: Date, Date this test was taken.
    archive: Boolean, When true, this certificate will no longer appear in
        queries.
    """

    __tablename__ = 'certificate'
    certid = DB.Column(DB.Integer, primary_key=True)
    userid = DB.Column(DB.Integer, DB.ForeignKey('user.userid'),
                       nullable=False)
    examid = DB.Column(DB.Integer, DB.ForeignKey('exam.examid'),
                       nullable=False)
    correct = DB.Column(DB.Integer, nullable=False)
    possible = DB.Column(DB.Integer, nullable=False)
    testdate = DB.Column(DB.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    passed = DB.Column(DB.Boolean, nullable=False, default=False)
    archive = DB.Column(DB.Boolean, nullable=False, default=False)
