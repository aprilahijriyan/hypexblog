from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user
from marshmallow import fields
from zemfrog.decorators import authenticate, http_code
from zemfrog.globals import ma
from zemfrog.helper import db_add, db_delete, db_update
from zemfrog.models import DefaultResponseSchema

from models.Comment import Comment, Reply


class CreateReplySchema(ma.Schema):
    comment_id = fields.Integer(required=True)
    text = fields.String()


class ReadReplySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reply
        include_fk = True


class UpdateReplySchema(ma.Schema):
    comment_id = fields.Integer(required=True)
    text = fields.String()


class DeleteReplySchema(ma.Schema):
    comment_id = fields.Integer(required=True)


class LimitReplySchema(ma.Schema):
    comment_id = fields.Integer(required=True)
    offset = fields.Integer()
    limit = fields.Integer()


# @authenticate()
@use_kwargs(LimitReplySchema(), location="query")
@marshal_with(ReadReplySchema(many=True), 200)
def read(**kwds):
    """
    Read all data.
    """

    comment_id = kwds["comment_id"]
    offset = kwds.get("offset")
    limit = kwds.get("limit")
    data = (
        Reply.query.filter_by(comment_id=comment_id).offset(offset).limit(limit).all()
    )
    return data


@authenticate()
@use_kwargs(CreateReplySchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def create(**kwds):
    """
    Add data.
    """

    comment_id = kwds["comment_id"]
    comment = Comment.query.get(comment_id)
    if not comment:
        return {"code": 404, "message": "Comment not found"}

    kwds["user_id"] = current_user.id
    model = Reply(**kwds)
    db_add(model)
    return {"code": 200, "message": "Successfully added data."}


@authenticate()
@use_kwargs(UpdateReplySchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def update(id, **kwds):
    """
    Update data.
    """

    comment_id = kwds["comment_id"]
    model = Reply.query.filter_by(
        id=id, user_id=current_user.id, comment_id=comment_id
    ).first()
    if model:
        db_update(model, text=kwds["text"])
        status_code = 200
        message = "Successfully updating data."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


@authenticate()
@use_kwargs(DeleteReplySchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def delete(id, **kwds):
    """
    Delete data.
    """

    comment_id = kwds["comment_id"]
    model = Reply.query.filter_by(
        id=id, user_id=current_user.id, comment_id=comment_id
    ).first()
    if model:
        db_delete(model)
        status_code = 200
        message = "Data deleted successfully."

    else:
        status_code = 404
        message = "Data not found."

    return {"code": status_code, "message": message}


docs = {"tags": ["Reply"]}
endpoint = "reply"
url_prefix = "/reply"
routes = [
    ("/create", create, ["POST"]),
    ("/read", read, ["GET"]),
    ("/update/<id>", update, ["PUT"]),
    ("/delete/<id>", delete, ["DELETE"]),
]
