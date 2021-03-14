from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user
from marshmallow import Schema, fields, pre_dump
from zemfrog.decorators import authenticate, http_code
from zemfrog.helper import db_add, db_delete
from zemfrog.models import DefaultResponseSchema

from models.Article import Article
from models.Like import Dislike, Like
from models.user import User


class LikeSchema(Schema):
    article_id = fields.Integer(required=True)


class LikeResponseSchema(Schema):
    users = fields.List(fields.String(), required=True)
    total = fields.Integer(required=True)

    @pre_dump
    def load_response(self, data, **kwargs):
        users = []
        for u in data["users"]:
            nickname = User.query.get(u.user_id).nickname
            users.append(nickname)
        data["users"] = users
        return data


@authenticate()
@use_kwargs(LikeSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def post(**kwds):
    article_id = kwds.get("article_id")
    article = Article.query.filter_by(id=article_id).first()
    if article:
        kwds["user_id"] = current_user.id
        code = 200
        message = "Ok"
        model = Like.query.filter_by(**kwds).first()
        if not model:
            model = Like(**kwds)
            func = db_add
        else:
            func = db_delete

        func(model)
        model_dislike = Dislike.query.filter_by(**kwds).first()
        if model_dislike:
            db_delete(model_dislike)

    else:
        code = 404
        message = "Article not found"

    return {"code": code, "message": message}


@authenticate()
@use_kwargs(LikeSchema)
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def delete(**kwds):
    article_id = kwds.get("article_id")
    article = Article.query.filter_by(id=article_id).first()
    if article:
        kwds["user_id"] = current_user.id
        code = 200
        message = "Ok"
        model = Dislike.query.filter_by(**kwds).first()
        if not model:
            model = Dislike(**kwds)
            func = db_add
        else:
            func = db_delete

        func(model)
        model_like = Like.query.filter_by(**kwds).first()
        if model_like:
            db_delete(model_like)

    else:
        code = 404
        message = "Article not found"

    return {"code": code, "message": message}


@use_kwargs(LikeSchema)
@marshal_with(LikeResponseSchema, 200)
@http_code
def get_total_liked(**kwds):
    article_id = kwds.get("article_id")
    query = Like.query.filter_by(article_id=article_id)
    total = query.count()
    users = query.all()
    return {"total": total, "users": users}


@use_kwargs(LikeSchema)
@marshal_with(LikeResponseSchema, 200)
@http_code
def get_total_dislikes(**kwds):
    article_id = kwds.get("article_id")
    query = Dislike.query.filter_by(article_id=article_id)
    total = query.count()
    users = query.all()
    return {"total": total, "users": users}


docs = {"tags": ["Like"]}
endpoint = "like"
url_prefix = ""
routes = [
    ("/like-it", post, ["POST"]),
    ("/dislike", delete, ["DELETE"]),
    ("/total/likes", get_total_liked, ["POST"]),
    ("/total/dislikes", get_total_dislikes, ["POST"]),
]
