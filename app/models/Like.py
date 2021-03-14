from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr
from zemfrog.globals import db


class LikeMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def article_id(self):
        return Column(ForeignKey("article.id"), nullable=False)

    @declared_attr
    def user_id(self):
        return Column(ForeignKey("user.id"), nullable=False)


class Like(LikeMixin, db.Model):
    pass


class Dislike(LikeMixin, db.Model):
    pass
