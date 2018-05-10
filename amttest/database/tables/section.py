"""The section table."""
from .. import DB


class Section(DB.Model):
    """
    sectionid: Integer, The unique identifier for the section.
    name: Text, Name of the section as seen by the admin.
    examid: Integer, Related to the exam table. The exam where this section
        belongs.
    active_questions: Integer, The number of questions to use from this section
        for each exam.
    archive: Boolean, When true, the section will no longer appear in queries.
    """
    __tablename__ = 'section'
    sectionid = DB.Column(DB.Integer, primary_key=True, nullable=False)
    name = DB.Column(DB.Text, nullable=False)
    examid = DB.Column(DB.Integer, DB.ForeignKey('exam.examid'))
    active_questions = DB.Column(DB.Integer, default=0)
    archive = DB.Column(DB.Boolean, nullable=False, default=False)
