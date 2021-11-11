import os

class Config:

    
    SECRET_KEY = 'SwanSea06'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://claudbae:12345@localhost/pitch2'
    UPLOADED_PHOTOS_DEST ='app/static/photos'

#  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  
    pass

    # # simple mde  configurations
    # SIMPLEMDE_JS_IIFE = True
    # SIMPLEMDE_USE_CDN = True

class ProdConfig(Config):
     SQLALCHEMY_DATABASE_URI = 'postgres://xvxebaxxcjvapw:72bc31564ce584e521b12faff1c63f93878258e032f036bf24f811c84477a93f@ec2-3-225-30-189.compute-1.amazonaws.com:5432/d1d81n41hqp11q'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://claudbae:12345@localhost/pitch2_test'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://claudbae:12345@localhost/pitch2'
    DEBUG = True


config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}