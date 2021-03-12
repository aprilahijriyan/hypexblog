from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user
from marshmallow import fields
from zemfrog.decorators import authenticate, http_code
from zemfrog.globals import ma
from zemfrog.helper import db_add, db_delete, db_update
from zemfrog.models import DefaultResponseSchema

from models.Article import Article
from models.Comment import Comment


class CreateCommentSchema(ma.Schema):
    article_id = fields.Integer(required=True)
    text = fields.String(required=True)


class ReadCommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True


class UpdateCommentSchema(ma.Schema):
    article_id = fields.Integer(required=True)
    text = fields.String(required=True)


class DeleteCommentSchema(ma.Schema):
    article_id = fields.Integer(required=True)


class LimitCommentSchema(ma.Schema):
    article_id = fields.Integer(required=True)
    offset = fields.Integer()
    limit = fields.Integer()


# @authenticate()
@use_kwargs(LimitCommentSchema(), location="query")
@marshal_with(ReadCommentSchema(many=True), 200)
def read(**kwds):
    """
    Read all data.
    """

    article_id = kwds["article_id"]
    offset = kwds.get("offset")
    limit = kwds.get("limit")
    data = (
        Comment.query.filter_by(article_id=article_id).offset(offset).limit(limit).all()
    )
    return data


@authenticate()
@use_kwargs(CreateCommentSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def create(**kwds):
    """
    Add data.
    """

    article = Article.query.get(kwds["article_id"])
    if not article:
        return {"code": 404, "message": "Article not found"}

    kwds["user_id"] = current_user.id
    model = Comment(**kwds)
    db_add(model)
    return {"code": 200, "message": "Successfully added data."}


@authenticate()
@use_kwargs(UpdateCommentSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def update(id, **kwds):
    """
    Update data.
    """

    article_id = kwds["article_id"]
    text = kwds["text"]
    model = Comment.query.filter_by(
        id=id, user_id=current_user.id, article_id=article_id
    ).first()
    if model:
        db_update(model, text=text)
        status_code = 200
        message = "Successfully updating data."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


@authenticate()
@use_kwargs(DeleteCommentSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def delete(id):
    """
    Delete data.
    """

    article_id = kwds["article_id"]
    model = Comment.query.filter_by(
        id=id, user_id=current_user.id, article_id=article_id
    ).first()
    if model:
        db_delete(model)
        status_code = 200
        message = "Data deleted successfully."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


docs = {"tags": ["Comment"]}
endpoint = "comment"
url_prefix = "/comment"
routes = [
    ("/create", create, ["POST"]),
    ("/read", read, ["GET"]),
    ("/update/<id>", update, ["PUT"]),
    ("/delete/<id>", delete, ["DELETE"]),
]
