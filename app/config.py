from datetime import timedelta
from os import getenv


class Development(object):
    SECRET_KEY = "Your secret key!"
    DB_HOST = "localhost"
    DB_PORT = 5433
    DB_USER = getenv("POSTGRES_USER")
    DB_PASSWORD = getenv("POSTGRES_PASSWORD")
    DB_NAME = getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "JWT secret key!"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    MAIL_PORT = 8025
    MAIL_DEFAULT_SENDER = "admin@localhost.com"
    APISPEC_TITLE = "API Docs"
    APISPEC_SWAGGER_UI_URL = "/api/docs"
    APISPEC_SECURITY_DEFINITIONS = {
        "Bearer": {"type": "oauth2", "flow": "password", "tokenUrl": "/auth/jwt/login"}
    }
    APISPEC_SECURITY_PARAMS = [{"Bearer": []}]
    DEBUG = True
    APPS = []
    EXTENSIONS = [
        "zemfrog.extensions.sqlalchemy",
        "zemfrog.extensions.marshmallow",
        "zemfrog.extensions.migrate",
        "zemfrog.extensions.jwt",
        "zemfrog.extensions.mail",
        "zemfrog.extensions.celery",
        "zemfrog.extensions.apispec",
        "zemfrog.extensions.cors",
    ]
    COMMANDS = [
        "zemfrog.commands.api",
        "zemfrog.commands.blueprint",
        "zemfrog.commands.middleware",
        "zemfrog.commands.command",
        "zemfrog.commands.errorhandler",
        "zemfrog.commands.extension",
        "zemfrog.commands.model",
        "zemfrog.commands.task",
        # "zemfrog.commands.user",
        "zemfrog.commands.role",
        "zemfrog.commands.permission",
        "zemfrog.commands.loader",
        "zemfrog.commands.secretkey",
        "zemfrog.commands.context",
        "zemfrog.commands.filter",
        "zemfrog.commands.app",
        "reset",
        "user",
    ]
    BLUEPRINTS = ["auth"]
    STATICFILES = [("/media", "media", "media")]
    MIDDLEWARES = []
    APIS = [
        "Article",
        "User",
        "Comment",
        "Reply",
        "Like",
        "Bookmark",
        "Media",
        "Follower",
    ]
    ERROR_HANDLERS = {422: "api_errors", 400: "api_errors"}
    TASKS = []
    CONTEXT_PROCESSORS = []
    JINJA_FILTERS = []
    API_DOCS = True
    CREATE_DB = True
    USER_MODEL = "models.user.User"
    ROLE_MODEL = "models.user.Role"
    PERMISSION_MODEL = "models.user.Permission"
    LOADERS = [
        "zemfrog.loaders.extension",
        "zemfrog.loaders.staticfile",
        "zemfrog.loaders.model",
        "zemfrog.loaders.url",
        "zemfrog.loaders.blueprint",
        "zemfrog.loaders.middleware",
        "zemfrog.loaders.api",
        "zemfrog.loaders.error_handler",
        "zemfrog.loaders.command",
        "zemfrog.loaders.task",
        "zemfrog.loaders.openapi",
        "zemfrog.loaders.context_processor",
        "zemfrog.loaders.jinja_filter",
        "zemfrog.loaders.multiapp",
    ]
    REDIS_HOST = "redis"
    REDIS_PORT = 6380
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    CELERY_BROKER_URL = CELERY_RESULT_BACKEND
    # others
    ALLOWED_IMAGE_FILES = ("png", "jpg", "jpeg")
    MEDIA_DIR = "media/"


class Production(Development):
    DEBUG = False
    JWT_COOKIE_SECURE = True
    DB_HOST = "db"
    DB_USER = getenv("POSTGRES_USER")
    DB_PASSWORD = getenv("POSTGRES_PASSWORD")
    DB_NAME = getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    CELERY_BROKER_URL = CELERY_RESULT_BACKEND


class Testing(Development):
    TESTING = True
