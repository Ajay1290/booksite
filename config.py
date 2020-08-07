from datetime import timedelta
import json

class BaseConfig(object):
    DEBUG = False
    TESTING = False    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\LENOVO\\Desktop\\BookElf.in\\site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = 'DEBUG'
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = 'insecurekeyfordev'
    SEED_ADMIN_EMAIL = 'ajay@gmail.com'
    SEED_ADMIN_PASSWORD = 'apku1290'
    REMEMBER_COOKIE_DURATION = timedelta(days=1)

    LANGUAGES = {
        'en' : 'English',
        'kl' : 'Klingon'
    }
    BABEL_DEFAULT_LOCALE = 'en'

class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV='development'