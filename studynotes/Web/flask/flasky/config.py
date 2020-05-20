import os

DEFAULT_DB_URI = 'postgresql://127.0.0.1:5432/flasky'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'there is no need to initialize flask_wtf in app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.qq.com'
    # MAIL_PORT = int(os.environ.get('MAIL_PORT',587))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','true').lower() in ['true','on',1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '173371929@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'rwclpasgdjodbgjh'
    FLASKY_MAIL_SUBJECT_PREFIX = '[flasky]'
    MAIL_DEFAULT_SENDER = 'Flasky Admin <173371929@qq.com>' #username<email address>
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '173371929@qq.com'

    #-----------记录缓慢的数据库查询的配置
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or DEFAULT_DB_URI

class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or DEFAULT_DB_URI

class ProductionConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or DEFAULT_DB_URI

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}

