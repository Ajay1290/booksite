from datetime import timedelta
import json

class BaseConfig(object):
    DEBUG = False
    TESTING = False    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\ajayp\\Downloads\\booksite\\site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = 'DEBUG'
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = 'insecurekeyfordev'
    SEED_ADMIN_EMAIL = ''
    SEED_ADMIN_PASSWORD = ''
    REMEMBER_COOKIE_DURATION = timedelta(days=90)

    LANGUAGES = {
        'en' : 'English',
        'kl' : 'Klingon'
    }
    BABEL_DEFAULT_LOCALE = 'en'

class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV='development'