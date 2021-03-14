from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UnicodeText
from sqlalchemy.orm import relationship
from zemfrog.globals import db


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey("article.id"), nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    text = Column(UnicodeText, nullable=False)
    replies = relationship("Reply")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class Reply(db.Model):
    id = Column(Integer, primary_key=True)
    comment_id = Column(ForeignKey("comment.id"), nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", uselist=False)
    text = Column(UnicodeText, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
