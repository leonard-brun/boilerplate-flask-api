from flask_restful import Resource


class Version(Resource):
    def get(self):
        return {"version": "1.0"}
