from flask import Flask, render_template, make_response, request, session
from manager.ext import db, csrf, mail, login_manager, babel
from manager.apps.main.routes import main
from manager.apps.users.routes import users
from manager.apps.books.routes import books
from manager.apps.tags.routes import tags
from manager.apps.admins.routes import admins
from manager.apps.pages.routes import pages
from manager.apps.authors.routes import authors
from manager.models import *
from flask_login import current_user, AnonymousUserMixin
from celery import Celery

CELERY_TASK_LIST = [
    'manager.apps.users.tasks'
]

def create_celery_app(app=None):
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    
    app.config.from_object('config.DevConfig')

    with app.app_context():
        register_apps(app)
        extensions(app)
        authentication(app, Users)
        # locale(app)

        
    return app

def extensions(app):    
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    mail.init_app(app)

    return None


def register_apps(app):    
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(books)
    app.register_blueprint(tags)
    app.register_blueprint(authors)
    app.register_blueprint(pages)
    app.register_blueprint(admins)

    return None

def authentication(app, user_model):
    login_manager.login_view = 'users.login'
    login_manager.anonymous_user = MyAnonymousUser
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)


def locale(app):
    @babel.localeselector
    def get_locale():
        if current_user.is_authenticated:
            return current_user.locale

        accept_languages = app.config.get('LANGUAGES').keys()
        return request.accept_languages.best_match(accept_languages)


class MyAnonymousUser(AnonymousUserMixin):
    def __init__(self, **kwargs):        
        super(MyAnonymousUser, self).__init__(**kwargs)
        