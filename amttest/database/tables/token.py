from .. import db

class Token(db.Model):
    __tablename__ = 'token'
    token_id = db.Column(db.Integer, primary_key=True, nullable=False)
    token = db.Column(db.Text, nullable=False)
