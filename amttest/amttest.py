import argparse
import logging
import os

from flask import Flask
from logging import handlers

from .routes import certificate, question, section, test, user
from .errors import badrequest

from .helpers.bphandler import BPHandler


AMT_TEST = None


def config_app(name, urlbase_url='/amttest/api'):
    global AMT_TEST
    AMT_TEST = Flask(name)
    AMT_TEST.config['APPLICATION_ROOT'] = urlbase_url


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
    global AMT_TEST, CERT_BP
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
    args = parser.parse_args()
    setup_logging(args.debug, args.verbose)
    config_app('amttest')
    BPHandler.register_blueprints(AMT_TEST)
    AMT_TEST.run(debug=args.debug)
