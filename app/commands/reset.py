import click
from flask.cli import with_appcontext
from zemfrog.globals import db


@click.command()
@click.option("-a", "--all", is_flag=True, help="Drop the alembic_version table too")
@with_appcontext
def reset(all):
    """
    Drop all tables
    """

    print("Dropping all tables... ", end="")
    # rfc: https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
    db.session.remove()
    db.drop_all()
    if all:
        # rfc:
        # * https://stackoverflow.com/questions/57169757/how-to-directly-access-sqlite-database-to-delete-alembic-version-table
        # * https://stackoverflow.com/questions/17972020/how-to-execute-raw-sql-in-flask-sqlalchemy-app
        db.engine.execute("DROP TABLE IF EXISTS alembic_version;")

    print("(done)")


command = reset
