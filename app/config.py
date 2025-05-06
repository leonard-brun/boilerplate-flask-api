import os


class Config(object):
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("EXTERNAL_DB_URL") or "postgresql+psycopg2://postgres:root@db/boilerplate"


class ProductionConfig(Config):
    ENV = "production"


class DevelopmentConfig(Config):
    ENV = "development"

    # AWS
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")


class TestingConfig(Config):
    ENV = "test"

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:root@db_test/boilerplate"


CONFIG_MAP = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "default": DevelopmentConfig,
}
