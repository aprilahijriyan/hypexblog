from zemfrog.globals import db
from sqlalchemy import Column, Integer, ForeignKey, UnicodeText, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Bookmark(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    name = Column(UnicodeText, nullable=False)
    articles = relationship("Article")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
