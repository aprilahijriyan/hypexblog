from sqlalchemy import Column, ForeignKey, Integer, UnicodeText
from sqlalchemy.orm import relationship
from zemfrog.globals import db
from zemfrog.mixins import LogMixin, PermissionMixin, RoleMixin, UserMixin


class User(UserMixin, db.Model):
    nickname = Column(UnicodeText)
    profile_image = Column(UnicodeText)
    cover_image = Column(UnicodeText)
    roles = relationship("Role", secondary="role_links", lazy="dynamic")
    following = relationship(
        "User",
        secondary="follower_links",
        primaryjoin="User.id == FollowerLinks.user_id",
        secondaryjoin="User.id == FollowerLinks.following_id",
        backref="followers",
    )


class Role(RoleMixin, db.Model):
    permissions = relationship(
        "Permission", secondary="permission_links", lazy="dynamic"
    )


class RoleLinks(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    role_id = Column(ForeignKey("role.id"))


class Permission(PermissionMixin, db.Model):
    pass


class PermissionLinks(db.Model):
    id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey("role.id"))
    permission_id = Column(ForeignKey("permission.id"))


class Log(LogMixin, db.Model):
    pass
