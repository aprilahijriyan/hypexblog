from zemfrog.app import create_app, make_celery

app = create_app("wsgi")
celery = make_celery(app)