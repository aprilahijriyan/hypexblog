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
    user_id = Column(ForeignKey("user.id"))
    title = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True)
    image = Column(UnicodeText)
    text = Column(UnicodeText)
    drafted = Column(Boolean, default=False)
    tags = relationship("Tag")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
