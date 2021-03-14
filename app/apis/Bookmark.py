from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user
from marshmallow import fields
from zemfrog.decorators import authenticate, http_code
from zemfrog.globals import ma
from zemfrog.helper import db_add, db_commit, db_delete, db_update
from zemfrog.models import DefaultResponseSchema

from apis.Article import ReadArticleSchema
from models.Article import Article
from models.Bookmark import Bookmark


class CreateBookmarkSchema(ma.Schema):
    name = fields.String()
    articles = fields.List(fields.Integer())


class ReadBookmarkSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime("%d-%m-%Y %H:%M:%S")
    updated_at = fields.DateTime("%d-%m-%Y %H:%M:%S")


class UpdateBookmarkSchema(ma.Schema):
    name = fields.String()


# class DeleteBookmarkSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Bookmark


class ArticleIDSchema(ma.Schema):
    article_id = fields.Integer(required=True)


class LimitBookmarkSchema(ma.Schema):
    offset = fields.Integer()
    limit = fields.Integer()


@authenticate()
@use_kwargs(LimitBookmarkSchema(), location="query")
@marshal_with(ReadBookmarkSchema(many=True), 200)
def read(**kwds):
    """
    Read all data.
    """

    offset = kwds.get("offset")
    limit = kwds.get("limit")
    data = (
        Bookmark.query.filter_by(user_id=current_user.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return data


@authenticate()
@use_kwargs(CreateBookmarkSchema())
@marshal_with(DefaultResponseSchema, 200)
@http_code
def create(**kwds):
    """
    Add data.
    """

    status_code = 200
    message = "Successfully added data."
    articles = []
    for a in kwds.get("articles", []):
        a = Article.query.filter_by(id=a).first()
        if a:
            articles.append(a)

    cols = {"user_id": current_user.id, "name": kwds["name"]}
    model = Bookmark.query.filter_by(**cols).first()
    if model:
        for a in articles:
            exist = model.articles.filter_by(id=a.id).first()
            if not exist:
                model.articles.append(a)
        db_commit()

    else:
        cols["articles"] = articles
        model = Bookmark(**cols)
        db_add(model)

    return {"code": status_code, "message": message}


@authenticate()
@use_kwargs(UpdateBookmarkSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def update(id, **kwds):
    """
    Update data.
    """

    model = Bookmark.query.filter_by(id=id, user_id=current_user.id).first()
    if model:
        db_update(model, name=kwds["name"])
        status_code = 200
        message = "Successfully updating data."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


@authenticate()
# @use_kwargs(DeleteBookmarkSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def delete(id):
    """
    Delete data.
    """

    model = Bookmark.query.filter_by(id=id, user_id=current_user.id).first()
    if model:
        db_delete(model)
        status_code = 200
        message = "Data deleted successfully."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


@authenticate()
@use_kwargs(LimitBookmarkSchema(), location="query")
@marshal_with(ReadArticleSchema(many=True), 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def read_article(id, **kwds):
    offset = kwds.get("offset")
    limit = kwds.get("limit")
    model = Bookmark.query.filter_by(id=id, user_id=current_user.id).first()
    if model:
        articles = model.articles.offset(offset).limit(limit).all()
        return articles

    return {"code": 404, "message": "Data not found."}


@authenticate()
@use_kwargs(ArticleIDSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def delete_article(id, **kwds):
    model = Bookmark.query.filter_by(id=id, user_id=current_user.id).first()
    status_code = 404
    message = "Data not found."
    if model:
        article = model.articles.filter_by(id=kwds["article_id"]).first()
        if article:
            model.articles.remove(article)
            db_commit()

        status_code = 200
        message = "Ok"

    return {"code": status_code, "message": message}


docs = {"tags": ["Bookmark"]}
endpoint = "bookmark"
url_prefix = "/bookmark"
routes = [
    ("/create", create, ["POST"]),
    ("/read", read, ["GET"]),
    ("/update/<id>", update, ["PUT"]),
    ("/delete/<id>", delete, ["DELETE"]),
    ("/read/article/<id>", read_article, ["GET"]),
    ("/delete/article/<id>", delete_article, ["DELETE"]),
]
