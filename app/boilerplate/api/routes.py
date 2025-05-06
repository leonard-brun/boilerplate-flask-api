from flask import Blueprint
from flask_restful import Api

from boilerplate.api.misc.resources import Version

blueprint = Blueprint("api", __name__)
api = Api(blueprint)

api.add_resource(Version, "/")
