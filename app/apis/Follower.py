from flask_jwt_extended import current_user
from flask_apispec import use_kwargs, marshal_with
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from zemfrog.decorators import authenticate
from zemfrog.models import DefaultResponseSchema
from zemfrog.helper import db_commit, db_delete
from models.user import User
from models.Follower import FollowerLinks


class FollowSchema(Schema):
    nickname = fields.String(required=True)


class UserFollowerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("nickname",)


@authenticate()
@use_kwargs(FollowSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
def post(**kwds):
    nickname = kwds["nickname"]
    user = User.query.filter_by(nickname=nickname).first()
    if user:
        status_code = 200
        message = "Ok"
        query = FollowerLinks.query.filter_by(
            user_id=current_user.id, following_id=user.id
        )
        if query.count() == 0:
            user.followers.append(current_user)
            db_commit()
    else:
        status_code = 404
        message = "User not found"

    return {"code": status_code, "message": message}


@authenticate()
@use_kwargs(FollowSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
def delete(**kwds):
    nickname = kwds["nickname"]
    user = User.query.filter_by(nickname=nickname).first()
    if user:
        status_code = 200
        message = "Ok"
        model = FollowerLinks.query.filter_by(
            user_id=current_user.id, following_id=user.id
        ).first()
        if model:
            db_delete(model)
    else:
        status_code = 404
        message = "User not found"

    return {"code": status_code, "message": message}


@authenticate()
@marshal_with(UserFollowerSchema(many=True), 200)
def get_followers():
    return current_user.followers


@authenticate()
@marshal_with(UserFollowerSchema(many=True), 200)
def get_following():
    return current_user.following


docs = {"tags": ["Follower"]}
endpoint = "follower"
url_prefix = ""
routes = [
    ("/follow", post, ["POST"]),
    ("/unfollow", delete, ["DELETE"]),
    ("/followers", get_followers, ["GET"]),
    ("/following", get_following, ["GET"]),
]
