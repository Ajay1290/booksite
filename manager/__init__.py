from flask import Flask, render_template, make_response, request, session
from manager.ext import db, csrf, mail, login_manager, babel, limiter
from manager.apps.main.routes import main
from manager.apps.users.routes import users
from manager.apps.books.routes import books
from manager.apps.tags.routes import tags
from manager.apps.admins.routes import admins
from manager.apps.pages.routes import pages
from manager.apps.authors.routes import authors
import logging
from werkzeug.middleware.proxy_fix import ProxyFix
from logging.handlers import SMTPHandler
from manager.models import *
from flask_login import current_user
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

def create_app(settings_override=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_object('config.DevConfig')
    # app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    with app.app_context():
        middleware(app)
        error_templates(app)
        exception_handler(app)
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
    limiter.init_app(app)

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

        
def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Swap request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)

    return None


def exception_handler(app):
    """
    Register 0 or more exception handlers (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail_handler = SMTPHandler((app.config.get('MAIL_SERVER'),
                                app.config.get('MAIL_PORT')),
                               app.config.get('MAIL_USERNAME'),
                               [app.config.get('MAIL_USERNAME')],
                               '[Exception handler] A 5xx was thrown',
                               (app.config.get('MAIL_USERNAME'),
                                app.config.get('MAIL_PASSWORD')),
                               secure=())

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter("""
    Time:               %(asctime)s
    Message type:       %(levelname)s


    Message:

    %(message)s
    """))
    app.logger.addHandler(mail_handler)

    return None
