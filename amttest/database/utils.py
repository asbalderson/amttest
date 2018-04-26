from . import db
from .tables import *
from sqlalchemy import inspect

def create_tables():
    db.create_all()


def table2dict(table):
    return {attr.key: getattr(table, attr.key)
            for attr in inspect(table).mapper.column_attrs}