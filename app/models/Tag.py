from zemfrog.globals import db
from sqlalchemy import Column, Integer, ForeignKey, String

class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    article_id = Column(ForeignKey("article.id"))
    name = Column(String(60), nullable=False)
