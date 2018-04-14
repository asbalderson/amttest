import logging

from flask import Flask
from logging import handlers

AMT_TEST = None


def config_app(name=__name__, static_url='amttest/api/')
    global AMT_TEST
    AMT_TEST = Flask(name, static_url_path=static_url)


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
