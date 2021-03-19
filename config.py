from datetime import timedelta
import json

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///F:\\BookElf Versions\\Bookelf.in\\site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = 'DEBUG'
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = 'insecurekeyfordev'
    SEED_ADMIN_EMAIL = 'ajay@gmail.com'
    SEED_ADMIN_PASSWORD = 'apku1290'
    REMEMBER_COOKIE_DURATION = timedelta(days=1)

    # Celery.
    CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5
    # CELERYBEAT_SCHEDULE = {
    #     'mark-soon-to-expire-credit-cards': {
    #         'task': 'snakeeyes.blueprints.billing.tasks.mark_old_credit_cards',
    #         'schedule': crontab(hour=0, minute=0)
    #     },
    #     'expire-old-coupons': {
    #         'task': 'snakeeyes.blueprints.billing.tasks.expire_old_coupons',
    #         'schedule': crontab(hour=0, minute=1)
    #     },
    # }

    LANGUAGES = {
        'en' : 'English',
        'kl' : 'Klingon'
    }
    BABEL_DEFAULT_LOCALE = 'en'

    RATELIMIT_STORAGE_URL = CELERY_BROKER_URL
    RATELIMIT_STRATEGY = 'fixed-window-elastic-expiry'
    RATELIMIT_HEADERS_ENABLED = True

class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV='development'