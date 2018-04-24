from ..database import db
from ..database.tables.answer import Answer
from ..database.tables.question import Question
from ..database.tables.section import Section
from ..database.tables.test import Test

import csv
import collections
import logging
import os


def import_file(file_path, testname):
    """
    Import a csv file of questions into the database.
    :param file_path: String, path to the csv file to import
    :param testname: String, name of the test to import questions to
    :return: None
    """
    logger = logging.getLogger()
    if not os.path.exists(file_path):
        logger.error('cannot find file %s', file_path)
        raise OSError()

    testid = get_test_id(testname)

    with open(file_path) as csvfile:
        data = csv.DictReader(csvfile)

        sections = collections.defaultdict(set)
        questions = collections.defaultdict(list)

        for row in data:
            answer = {}
            answer['answer'] = row['answer']
            if row['correct'].lower() == 'true':
                answer['correct'] = True
            else:
                answer['correct'] = False
            questions[row['question']].append(answer)
            sections[row['section']].add(row['question'])

        for section in sections.copy().keys():
            sectionid = get_section_id(section, testid)
            for question in sections[section]:
                question_id = get_question_id(question, sectionid)
                for answer in questions[question]:
                    answer['questionid'] = question_id
                    new_answer(answer)


def get_test_id(testname):
    """
    Get a test id, or create one if it does not exist.
    :param testname: String, name of test to find id for
    :return: int, id for the test
    """
    logger = logging.getLogger(__name__)
    result = Test.query.filter_by(name=testname).first()
    if result:
        logger.info('Found test, id is: %s', result.testid)
        return result.testid
    new = Test(name=testname)
    db.session.add(new)
    db.session.commit()
    db.session.refresh(new)
    logger.info('New test created: %s', new)
    return new.testid


def get_section_id(sectionname, testid):
    """
    Get a section id or crate it if it does not exist.
    :param sectionname: String, Name of the section to get the id for
    :param testid: Int, when creating a new section, test to associate the section with
    :return: Int, id for the new section
    """
    logger = logging.getLogger(__name__)
    result = Section.query.filter_by(name=sectionname).first()
    if result:
        logger.info('Found section, id is: %s', result.sectionid)
        return result.sectionid
    new = Section(name=sectionname, testid=testid)
    db.session.add(new)
    db.session.commit()
    db.session.refresh(new)
    logger.info('New section created: %s', new)
    return new.sectionid


def get_question_id(question, sectionid):
    """
    Get a question id or create one, if it does not exist
    :param question: String, Text for the question
    :param sectionid: Int, if creating, the section id to associate the question to
    :return: None
    """
    logger = logging.getLogger(__name__)
    result = Question.query.filter_by(question=question).first()
    if result:
        logger.info('Found question, id is: %s', result.questionid)
        return result.questionid
    new = Question(question=question, sectionid=sectionid)
    db.session.add(new)
    db.session.commit()
    db.session.refresh(new)
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
    db.session.add(new)
    db.session.commit()
    db.session.refresh(new)
    logger.info('New answer created: %s', new)