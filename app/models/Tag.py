from sqlalchemy import Column, Integer, String
from zemfrog.globals import db


class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
