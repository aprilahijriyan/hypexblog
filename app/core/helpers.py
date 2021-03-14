import os
from distutils.dir_util import remove_tree
from hashlib import md5

from filetype import is_image
from flask import current_app
from werkzeug.utils import secure_filename


def get_extension(filename):
    ext = filename.rsplit(".", 1)[1]
    return ext


def is_image_file(filename, buffer):
    if (
        "." in filename
        and get_extension(filename) in current_app.config["ALLOWED_IMAGE_FILES"]
        and is_image(buffer)
    ):
        return True
    return False


def get_file_hash(filename, salt):
    char = f"{filename}+{salt}".encode()
    encrypted = md5(char).hexdigest()
    return encrypted


def delete_file_media(*files):
    filedst = os.path.join(current_app.config["MEDIA_DIR"], *files)
    if os.path.isfile(filedst):
        os.remove(filedst)
        return True

    elif os.path.isdir(filedst):
        remove_tree(filedst)
        return True

    return False


def save_to(filename, buffer, email, outdir=None):
    filename = secure_filename(filename)
    ext = get_extension(filename)
    filehash = get_file_hash(filename, email) + "." + ext
    media_dir = current_app.config["MEDIA_DIR"]
    output_dir = media_dir
    if outdir is not None:
        output_dir = os.path.join(output_dir, outdir)
        os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, filehash)
    with open(output_file, "wb") as fp:
        fp.write(buffer)

    return output_file[len(media_dir) :]
