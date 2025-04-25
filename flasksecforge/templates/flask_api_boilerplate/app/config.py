import os
from dotenv import load_dotenv

load_dotenv()  # read .env

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}