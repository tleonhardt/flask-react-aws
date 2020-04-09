# project/api/ping.py


from flask_restx import Namespace, Resource

ping_namespace = Namespace("ping")


@ping_namespace.route('')
class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}
