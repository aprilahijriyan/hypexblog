from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
)
from sqlalchemy.orm import relationship
from zemfrog.globals import db


class Article(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True)
    image = Column(UnicodeText)
    text = Column(UnicodeText)
    drafted = Column(Boolean, default=True)
    tags = relationship("Tag", secondary="tag_links", lazy="dynamic")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class TagLinks(db.Model):
    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey("article.id"))
    tag_id = Column(ForeignKey("tag.id"))
