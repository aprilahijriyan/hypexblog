from zemfrog.globals import db
from zemfrog.mixins import UserMixin, RoleMixin, PermissionMixin, LogMixin
from sqlalchemy import Column, UnicodeText
from sqlalchemy.orm import relationship


class User(UserMixin, db.Model):
    nickname = Column(UnicodeText)
    profile_image = Column(UnicodeText)
    cover_image = Column(UnicodeText)
    articles = relationship("Article")


class Role(RoleMixin, db.Model):
    pass


class Permission(PermissionMixin, db.Model):
    pass


class Log(LogMixin, db.Model):
    pass
