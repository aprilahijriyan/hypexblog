from flask import url_for
from flask_jwt_extended import current_user
from marshmallow import ValidationError
from werkzeug.datastructures import FileStorage

from core.helpers import is_image_file, save_to


def save_image_file(filestorage: FileStorage):
    filename = filestorage.filename
    buffer = filestorage.stream.read()
    if not is_image_file(filename, buffer):
        raise ValidationError("This is not an image file")

    output_file = save_to(
        filename, buffer, current_user.email, outdir=current_user.nickname
    )
    url = url_for("media", filename=output_file)
    return url
