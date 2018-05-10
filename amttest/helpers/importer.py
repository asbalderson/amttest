"""
Methods for importing a csv file into the database.
An example file can be found in the /data directory.
"""
import csv
import collections
import logging
import os

from ..database import DB
from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..database.tables.exam import Exam


def import_file(file_path, examname):
    """
    Import a csv file of questions into the database.
    :param file_path: String, path to the csv file to import
    :param examname: String, name of the test` to import questions to
    :return: None
    """
    logger = logging.getLogger()
    if not os.path.exists(file_path):
        logger.error('cannot find file %s', file_path)
        raise OSError()

    examid = get_exam_id(examname)

    with open(file_path) as csvfile:
        data = csv.DictReader(csvfile)

        sections = collections.defaultdict(set)
        questions = collections.defaultdict(list)

        for row in data:
            answer = {}
            answer['answer'] = row['answer']
            answer['correct'] = row['correct'].lower() == 'true'
            questions[row['question']].append(answer)
            sections[row['section']].add(row['question'])

        for section in sections.copy().keys():
            sectionid = get_section_id(section, examid)
            for question in sections[section]:
                question_id = get_question_id(question, sectionid)
                for answer in questions[question]:
                    answer['questionid'] = question_id
                    new_answer(answer)


def get_exam_id(examname):
    """
    Get a test id, or create one if it does not exist.
    :param testname: String, name of test to find id for
    :return: int, id for the test
    """
    logger = logging.getLogger(__name__)
    result = Exam.query.filter_by(name=examname).first()
    if result:
        logger.info('Found exam, id is: %s', result.examid)
        return result.examid
    new = Exam(name=examname)
    DB.session.add(new)
    DB.session.commit()
    DB.session.refresh(new)
    logger.info('New exam created: %s', new)
    return new.examid


def get_section_id(sectionname, examid):
    """
    Get a section id or crate it if it does not exist.
    :param sectionname: String, Name of the section to get the id for
    :param testid: Int, when creating a new section, test to associate
    the section with
    :return: Int, id for the new section
    """
    logger = logging.getLogger(__name__)
    result = Section.query.filter_by(name=sectionname).first()
    if result:
        logger.info('Found section, id is: %s', result.sectionid)
        return result.sectionid
    new = Section(name=sectionname, examid=examid)
    DB.session.add(new)
    DB.session.commit()
    DB.session.refresh(new)
    logger.info('New section created: %s', new)
    return new.sectionid


def get_question_id(question, sectionid):
    """
    Get a question id or create one, if it does not exist
    :param question: String, Text for the question
    :param sectionid: Int, if creating, the section id to associate the
    question to
    :return: None
    """
    logger = logging.getLogger(__name__)
    result = Question.query.filter_by(question=question).first()
    if result:
        logger.info('Found question, id is: %s', result.questionid)
        return result.questionid
    new = Question(question=question, sectionid=sectionid)
    DB.session.add(new)
    DB.session.commit()
    DB.session.refresh(new)
    logger.info('New question created: %s', new)
    return new.questionid


def new_answer(answerdict):
    """
    Create a new answer in the database
    :param answerdict: dict, keyvalue pairs for answer key names
    :return: None
    """
    logger = logging.getLogger(__name__)
    new = Answer(**answerdict)
    DB.session.add(new)
    DB.session.commit()
    DB.session.refresh(new)
    logger.info('New answer created: %s', new)
