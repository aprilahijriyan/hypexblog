from zemfrog.globals import db
from zemfrog.mixins import UserMixin, RoleMixin, PermissionMixin, LogMixin
from sqlalchemy.orm import relationship


class User(UserMixin, db.Model):
    articles = relationship("Article")


class Role(RoleMixin, db.Model):
    pass


class Permission(PermissionMixin, db.Model):
    pass


class Log(LogMixin, db.Model):
    pass