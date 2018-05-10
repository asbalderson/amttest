"""The exam table."""
from .. import DB


class Exam(DB.Model):
    """
    Exam table.

    examid: Integer, the exam's identifier, always unique.
    time_limit: Integer, The number of minutes given for the user to take
        the exam.
    name: Text, The plain text name of the exam.
    pass_percent: Integer, The whole number value required to pass the exam.
    expiration: Integer, The number of months the certifications from the exam
        are valid.
    ula: Text, What the user agrees to before they take the exam.
    archive: Boolean, When true, the exam will no longer be available from
        queries.
    """

    __tablename__ = 'exam'
    examid = DB.Column(DB.Integer, primary_key=True, nullable=False)
    time_limit = DB.Column(DB.Integer, nullable=False, default=20)
    name = DB.Column(DB.Text, nullable=False)
    pass_percent = DB.Column(DB.Integer, nullable=False, default=75)
    expiration = DB.Column(DB.Integer, nullable=False, default=12)
    ula = DB.Column(DB.Text, nullable=False, default='Do not cheat!')
    archive = DB.Column(DB.Boolean, nullable=False, default=False)
