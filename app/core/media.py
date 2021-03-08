from core.helpers import is_image_file, save_to
from marshmallow import ValidationError
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import current_user


def save_image_file(filestorage: FileStorage):
    filename = filestorage.filename
    buffer = filestorage.stream.read()
    if not is_image_file(filename, buffer):
        raise ValidationError("This is not an image file")

    output_file = save_to(
        filename, buffer, current_user.email, outdir=current_user.nickname
    )
    return output_file
