from . import db

from .tables import *


def create_tables():
    db.create_all()
