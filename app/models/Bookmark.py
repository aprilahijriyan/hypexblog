from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UnicodeText
from sqlalchemy.orm import relationship
from zemfrog.globals import db


class Bookmark(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    name = Column(UnicodeText, nullable=False)
    articles = relationship("Article", secondary="bookmark_links", lazy="dynamic")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class BookmarkLinks(db.Model):
    id = Column(Integer, primary_key=True)
    bookmark_id = Column(ForeignKey("bookmark.id"))
    article_id = Column(ForeignKey("article.id"))
