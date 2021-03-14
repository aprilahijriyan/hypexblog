from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user
from marshmallow import fields
from slugify import slugify
from zemfrog.decorators import authenticate, http_code
from zemfrog.globals import ma
from zemfrog.helper import db_add, db_delete, db_update
from zemfrog.models import DefaultResponseSchema

from models.Article import Article
from models.Tag import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String()


class CreateArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        fields = ("title", "image", "text", "drafted", "tags")

    image = fields.Url()
    tags = fields.List(fields.String())


class ReadArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        exclude = ("user_id", "drafted")

    tags = fields.List(fields.Nested(TagSchema()))
    created_at = fields.DateTime("%d-%m-%Y %H:%M:%S")
    updated_at = fields.DateTime("%d-%m-%Y %H:%M:%S")


class UpdateArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        fields = ("title", "image", "text", "drafted", "tags")

    image = fields.Url()
    text = fields.String()
    drafted = fields.Boolean()
    tags = fields.List(fields.String())


# class DeleteArticleSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Article


class LimitArticleSchema(ma.Schema):
    title = fields.String()
    text = fields.String()
    tags = fields.List(fields.String())
    offset = fields.Integer()
    limit = fields.Integer()


class MyReadArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        exclude = ("user_id",)


class MyLimitArticleSchema(LimitArticleSchema):
    drafted = fields.Boolean()


@authenticate()
@use_kwargs(MyLimitArticleSchema(), location="query")
@marshal_with(MyReadArticleSchema(many=True), 200)
def me(**kwds):
    """
    Read all data.
    """

    title = kwds.get("title")
    text = kwds.get("text")
    tags = kwds.get("tags")
    drafted = kwds.get("drafted")
    offset = kwds.get("offset")
    limit = kwds.get("limit")
    query = Article.query.filter_by(user_id=current_user.id)
    if title:
        query = query.filter(Article.title.contains(title))

    if text:
        query = query.filter(Article.text.contains(text))

    if tags:
        query = query.filter(Article.tags.any(Tag.name.in_(tags)))

    query = query.filter_by(drafted=drafted)
    data = query.offset(offset).limit(limit).all()
    return data


@use_kwargs(LimitArticleSchema(), location="query")
@marshal_with(ReadArticleSchema(many=True), 200)
def read(**kwds):
    """
    Read all data.
    """

    title = kwds.get("title")
    text = kwds.get("text")
    tags = kwds.get("tags")
    offset = kwds.get("offset")
    limit = kwds.get("limit")
    query = Article.query
    if title:
        query = query.filter(Article.title.contains(title))

    if text:
        query = query.filter(Article.text.contains(text))

    if tags:
        query = query.filter(Article.tags.any(Tag.name.in_(tags)))

    data = query.offset(offset).limit(limit).all()
    return data


@authenticate()
@use_kwargs(CreateArticleSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@http_code
def create(**kwds):
    """
    Add data.
    """

    found = Article.query.filter_by(title=kwds["title"]).first()
    if not found:
        tags = []
        for t in kwds.get("tags", []):
            t = t.capitalize()
            tag = Tag.query.filter_by(name=t).first()
            if not tag:
                tag = Tag(name=t)
                db_add(tag)
            tags.append(tag)

        kwds["tags"] = tags
        kwds["slug"] = slugify(kwds["title"])
        kwds["user_id"] = current_user.id
        model = Article(**kwds)
        db_add(model)
        status_code = 200
        message = "Successfully added data."

    else:
        status_code = 403
        message = "Data already exists."

    return {"code": status_code, "message": message}


@authenticate()
@use_kwargs(UpdateArticleSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def update(id, **kwds):
    """
    Update data.
    """

    model = Article.query.filter_by(user_id=current_user.id, id=id).first()
    if model:
        tags = []
        for t in kwds.get("tags", []):
            t = t.capitalize()
            tag = Tag.query.filter_by(name=t).first()
            if not tag:
                tag = Tag(name=t)
                db_add(tag)
            tags.append(tag)

        kwds["tags"] = tags
        kwds["slug"] = slugify(kwds["title"])
        db_update(model, **kwds)
        status_code = 200
        message = "Successfully updating data."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


@authenticate()
# @use_kwargs(DeleteArticleSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def delete(id):
    """
    Delete data.
    """

    model = Article.query.filter_by(user_id=current_user.id, id=id).first()
    if model:
        db_delete(model)
        status_code = 200
        message = "Data deleted successfully."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


docs = {"tags": ["Article"]}
endpoint = "article"
url_prefix = "/article"
routes = [
    ("/create", create, ["POST"]),
    ("/read", read, ["GET"]),
    ("/update/<id>", update, ["PUT"]),
    ("/delete/<id>", delete, ["DELETE"]),
    ("/me", me, ["GET"]),
]
