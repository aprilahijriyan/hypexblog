from core.helpers import is_image_file
from marshmallow import ValidationError
from io import BytesIO


def image_file_required(value):
    filename = value.filename
    buffer = value.stream.read()
    if not is_image_file(filename, buffer):
        raise ValidationError("This is not an image file")

    wrapper = BytesIO(buffer)
    value.stream = wrapper
