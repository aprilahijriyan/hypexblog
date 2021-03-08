from zemfrog.commands.user import group
from zemfrog.helper import db_commit
from models.user import User
from flask.cli import with_appcontext


@group.command()
@with_appcontext
def generate_nickname():
    """
    Generate nickname for all users
    """

    print("Creating a nickname for all users... ", end="")

    for user in User.query.all():
        name = user.name
        nickname = name.replace(" ", "").lower()
        user.nickname = nickname

    db_commit()
    print("(done)")


command = group
