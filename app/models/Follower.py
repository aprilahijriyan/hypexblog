from zemfrog.globals import db
from sqlalchemy import Column, Integer, ForeignKey


class FollowerLinks(db.Model):
    """
    Taken from https://stackoverflow.com/questions/23622922/how-to-implement-following-followers-relationship-in-sqlalchemy
    """

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    following_id = Column(ForeignKey("user.id"))
