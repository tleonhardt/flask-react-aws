# services/users/project/tests/test_auth.py


import json

import pytest


def test_user_registration(test_app, test_database, add_user):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps({
            "username": "justatest",
            "email": "test@test.com",
            "password": "123456",
        }),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert "justatest" in data["username"]
    assert "test@test.com" in data["email"]
    assert "password" not in data


def test_user_registration_duplicate_email(test_app, test_database, add_user):
    add_user("test", "test@test.com", "test")
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps({
            "username": "michael",
            "email": "test@test.com",
            "password": "test"
        }),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Sorry. That email already exists." in data["message"]


@pytest.mark.parametrize("payload",
    [
        [{}],                                                           # empty payload
        [{"email": "me@testdriven.io", "password": "greaterthanten"}],  # no username
        [{"username": "michael", "password": "greaterthanten"}],        # no email
        [{"email": "me@testdriven.io", "username": "michael"}],         # no password
    ],
)
def test_user_registration_invalid_json(test_app, test_database, payload):
    client = test_app.test_client()
    resp = client.post(
        f"/auth/register", data=json.dumps(payload), content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Input payload validation failed" in data["message"]


def test_registered_user_login(test_app, test_database, add_user):
    add_user("test3", "test3@test.com", "test")
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({
            "email": "test3@test.com",
            "password": "test"
        }),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_not_registered_user_login(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({
            "email": "testnotreal@test.com",
            "password": "test"
        }),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert resp.content_type == "application/json"
    assert "User does not exist." in data["message"]
