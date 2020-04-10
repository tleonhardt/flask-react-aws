# services/users/project/api/auth.py

import jwt
from flask import request
from flask_restx import Namespace, Resource, fields
from project import bcrypt
from project.api.users.crud import add_user, get_user_by_email, get_user_by_id
from project.api.users.models import User

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

login = auth_namespace.model(
    "User",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

refresh = auth_namespace.model(
    "Refresh", {"refresh_token": fields.String(required=True)}
)

tokens = auth_namespace.clone(
    "Access and refresh_tokens", refresh, {"access_token": fields.String(required=True)}
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
    """Authenitcate a user, returning access and refresh tokens."""
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(login, validate=True)
    @auth_namespace.response(200, "Success")
    @auth_namespace.response(404, "User does not exist")
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        user = get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password, password):
            auth_namespace.abort(404, "User does not exist")
        access_token = user.encode_token(user.id, "access")
        refresh_token = user.encode_token(user.id, "refresh")

        response_object = {
            "access_token": access_token.decode(),
            "refresh_token": refresh_token.decode()
        }
        return response_object, 200


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(refresh, validate=True)
    @auth_namespace.response(200, "Success")
    @auth_namespace.response(401, "Invalid token")
    def post(self):
        """Refresh an existing token."""
        post_data = request.get_json()
        refresh_token = post_data.get("refresh_token")
        response_object = {}

        try:
            resp = User.decode_token(refresh_token)
            user = get_user_by_id(resp)
            if not user:
                auth_namespace.abort(401, "Invalid token")
            access_token = user.encode_token(user.id, "access")
            refresh_token = user.encode_token(user.id, "refresh")

            response_object = {
                "access_token": access_token.decode(),
                "refresh_token": refresh_token.decode(),
            }
            return response_object, 200
        except jwt.ExpiredSignatureError:
            auth_namespace.abort(401, "Signature expired. Please log in again.")
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            auth_namespace.abort(401, "Invalid token. Please log in again.")


@auth_namespace.route('/status')
class Status(Resource):
    def get(self):
        pass