import argparse
import logging
import os

from flask import Flask
from logging import handlers

from .database import db
from .database.utils import create_tables
from .routes import *
from .errors import *

from .helpers.bphandler import BPHandler
from .helpers.token import gen_token, list_token
from .helpers.importer import import_file

def config_app(name, urlbase_url='/amttest/api'):
    app = Flask(name)
    app.config['APPLICATION_ROOT'] = urlbase_url
    return app


def config_dabase(app):
    global db
    app_path = '/var/cache/amttest'
    if not os.path.exists(app_path):
        os.mkdir(app_path)
    db_path = 'sqlite:///%s/amttest.db' % app_path
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def setup_logging(debug=False, verbose=False):
    logger = logging.getLogger()
    log_dir = '/var/log/amttest'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_name = os.path.join(log_dir, 'amttest.log')
    logger.setLevel(logging.WARNING)
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s %(levelname)s: %(message)s')

    term_channel = logging.StreamHandler()
    term_channel.setFormatter(formatter)
    logger.addHandler(term_channel)

    file_channel = handlers.RotatingFileHandler(file_name,
                                                maxBytes=4000000,
                                                backupCount=8)
    logger.addHandler(file_channel)


def launch_api():
    parser = argparse.ArgumentParser(description='Launch a API with routes for '
                                                 'a test application')
    parser.add_argument('-d', '--debug',
                        help='turn on the debug flag',
                        default=False,
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='turn on terminal output',
                        default=False,
                        action='store_true')
    subparser = parser.add_subparsers(dest='subcmd')
    subparser.required = True

    subparser.add_parser('init', help='setup the database')

    run = subparser.add_parser('run', help='run the app')

    run.add_argument('-p', '--port',
                     help='port to run the app on',
                     default=None)
    run.add_argument('-i', '--ip',
                     help='ip address to run the host at',
                     default=None)
    token = subparser.add_parser('token', help='generate a fresh token')
    token.add_argument('-l', '--list',
                      help='List all current tokens',
                      default=False,
                      action='store_true')
    importer = subparser.add_parser('import',
                                    help='import questions from a csv file')
    importer.add_argument('file',
                          help='File to import questions from, '
                               'needs to be a csv file, and have the following '
                               'headers in the following order:\n'
                               'section: Name of the section the question belongs \n'
                               'question: the question being asked \n'
                               'answer: an answer for that question \n'
                               'correct: TRUE for correct, FALSE for incorrect')
    importer.add_argument('test',
                          help='test to import the questions for ex:\n'
                               '\t"Reeves Test"'
                               '\t"Corpra Test"')
    args = parser.parse_args()
    cmd = vars(args).pop('subcmd')
    setup_logging(args.debug, args.verbose)
    app = config_app('amttest')
    BPHandler.register_blueprints(app)
    config_dabase(app)
    if cmd == 'run':
        app.run(debug=args.debug, port=args.port)
    elif cmd =='init':
        create_tables()
    elif cmd == 'token':
        if args.list:
            list_token()
        else:
            gen_token()
    elif cmd == 'import':
        import_file(args.file, args.test)