from .. import db


class Test(db.Model):
    __tablename__ = 'test'
    testid = db.Column(db.Integer, primary_key=True, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    test_name = db.Column(db.Text, nullable=False)
    pass_percent = db.Column(db.Integer, nullable=False)
    expiration = db.Column(db.Integer, nullable=False)
    ula = db.Column(db.Text, nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)
