from .. import db


class Test(db.Model):
    __tablename__ = 'test'
    testid = db.Column(db.Integer, primary_key=True, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False, default=20)
    name = db.Column(db.Text, nullable=False)
    pass_percent = db.Column(db.Integer, nullable=False, default=75)
    expiration = db.Column(db.Integer, nullable=False, default='12')
    ula = db.Column(db.Text, nullable=False, default='Do not cheat!')
    archive = db.Column(db.Boolean, nullable=False, default=False)
