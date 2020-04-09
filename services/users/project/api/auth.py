# services/users/project/api/auth.py

from flask import request
from flask_restx import Namespace, Resource, fields

from project.api.users.crud import get_user_by_email, get_user_by_id, add_user

auth_namespace = Namespace("auth")

user_model = auth_namespace.model(
    "User",
    {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
    },
)

full_user = auth_namespace.clone(
    "Full User", user_model, {"password": fields.String(required=True)}
)


@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.expect(full_user, validate=True)
    @auth_namespace.response(201, "Success")
    @auth_namespace.response(400, "Sorry. That email already exists.")
    def post(self):
        """Register a new user for authentication."""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")

        user = get_user_by_email(email)
        if user:
            auth_namespace.abort(400, "Sorry. That email already exists.")
        user = add_user(username, email, password)
        return user, 201


@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        pass


@auth_namespace.route('/refresh')
class Refresh(Resource):
    def post(self):
        pass


@auth_namespace.route('/status')
class Status(Resource):
    def get(self):
        pass
