from .. import db

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, nullable=False)
    fbuserid = db.Column(db.Integer, nullable=False)
    amt_name = db.Column(db.Text, default='')
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    kingdom = db.Column(db.Text, default='')
    admin = db.Column(db.Boolean, default=False, nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)
