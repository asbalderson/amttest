"""The user table."""
from .. import DB


class User(DB.Model):
    """
    User table.

    userid: Integer, generated user identifier for each user, always unique.
    amt_name: Text, A users amtgard persona name, not required, good to have.
    name: Text, The users real name.
    email: Text, The users email address.
    kingdom: Text, The kingdom that the user is a member of.
    admin: Boolean, When true, the user can access the admin panel.
    archive: Boolean, When true, the user is no longer available for viewing.
    """

    __tablename__ = 'user'
    userid = DB.Column(DB.Integer, primary_key=True, nullable=False)
    amt_name = DB.Column(DB.Text, default='')
    name = DB.Column(DB.Text, nullable=False)
    email = DB.Column(DB.Text, nullable=False)
    kingdom = DB.Column(DB.Text, default='')
    admin = DB.Column(DB.Boolean, default=False, nullable=False)
    archive = DB.Column(DB.Boolean, nullable=False, default=False)
