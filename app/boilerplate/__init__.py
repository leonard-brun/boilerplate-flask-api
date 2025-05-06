import os
import logging
from marshmallow import ValidationError
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from contextlib import contextmanager
from config import CONFIG_MAP


logger = logging.getLogger(__name__)

ma = Marshmallow()
db = SQLAlchemy()


def create_app(env=None):
    app = Flask(__name__)

    env = env or os.environ.get("ENV", "default")
    app.config.from_object(CONFIG_MAP.get(env, "default"))

    db.init_app(app)
    ma.init_app(app)
    init_converters(app)
    Migrate(app, db)
    CORS(app)

    from boilerplate.api.routes import blueprint as api_blueprint
    app.register_blueprint(api_blueprint)

    app.register_error_handler(Exception, server_error_handler)
    app.register_error_handler(500, server_error_handler)
    app.register_error_handler(404, resource_error_handler)
    return app


def resource_error_handler(error):
    return jsonify({"message": "Resource not found.", "error": "not_found"}), 404


def server_error_handler(error):
    if isinstance(error, ValidationError):
        return jsonify({"errors": error.messages}), 422

    logger.exception(error)
    return jsonify({"message": "Internal error.", "error": "internal_error"}), 500


def init_converters(app):
    pass


@contextmanager
def transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
