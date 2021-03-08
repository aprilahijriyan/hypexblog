from zemfrog.decorators import http_code, authenticate
from zemfrog.helper import db_delete, db_update
from flask_jwt_extended import current_user
from zemfrog.extensions.apispec import FileField
from zemfrog.models import DefaultResponseSchema
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields, validates, ValidationError
from zemfrog.globals import ma
from models.user import User, Role, Permission
from zemfrog.validators import validate_password_length, validate_username
from core.media import save_image_file


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role

    permissions = fields.List(fields.Nested(PermissionSchema()))


class ReadUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password",)

    confirmed_at = fields.DateTime("%d-%m-%Y %H:%M:%S")
    register_at = fields.DateTime("%d-%m-%Y %H:%M:%S")
    roles = fields.List(fields.Nested(RoleSchema()))


class UpdateUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()

    @validates("first_name")
    def validate_first_name(self, value):
        if value and not validate_username(value, silently=True):
            raise ValidationError("First name must be a character [a-zA-Z]")

    @validates("last_name")
    def validate_last_name(self, value):
        if value and not validate_username(value, silently=True):
            raise ValidationError("Last name must be a character [a-zA-Z]")

    @validates("password")
    def validate_password(self, value):
        if value and not validate_password_length(value, silently=True):
            raise ValidationError("Password length must be greater than or equal to 8")


class FileUploadSchema(ma.Schema):
    profile_image = FileField(validate=save_image_file)
    cover_image = FileField(validate=save_image_file)


@authenticate()
@marshal_with(ReadUserSchema(), 200)
def detail():
    """
    Read user data.
    """

    return current_user


@authenticate()
@use_kwargs(UpdateUserSchema(), location="form")
@use_kwargs(FileUploadSchema(), location="files")
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 403)
@http_code
def update(**kwds):
    """
    Update data.
    """

    print(kwds)
    first_name = kwds.get("first_name", current_user.first_name)
    last_name = kwds.get("last_name", current_user.last_name)
    name = first_name + " " + last_name
    kwds["name"] = name
    profile_image = kwds.get("profile_image")
    if profile_image:
        profile_image = save_image_file(profile_image)
        kwds["profile_image"] = profile_image

    cover_image = kwds.get("cover_image")
    if cover_image:
        cover_image = save_image_file(cover_image)
        kwds["cover_image"] = cover_image

    db_update(current_user, **kwds)
    status_code = 200
    message = "Successfully updating data."
    return {"code": status_code, "message": message}


@authenticate()
# @use_kwargs(DeleteUserSchema())
@marshal_with(DefaultResponseSchema, 200)
@marshal_with(DefaultResponseSchema, 404)
@http_code
def delete():
    """
    Delete data.
    """

    db_delete(current_user)
    status_code = 200
    message = "Data deleted successfully."
    return {"code": status_code, "message": message}


docs = {"tags": ["User"]}
endpoint = "user"
url_prefix = "/user"
routes = [
    ("/detail", detail, ["GET"]),
    ("/update", update, ["PUT"]),
    ("/delete", delete, ["DELETE"]),
]
