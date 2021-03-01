import os
import jwt
from flask.testing import FlaskClient
from fakeredis import FakeStrictRedis


def test_register(client: FlaskClient, redis_client: FakeStrictRedis):
    # Empty request
    res = client.post("/account")
    assert res.status_code == 400

    # No data
    res = client.post("/account")
    assert res.status_code == 400

    # Proper data
    res = client.post("/account", json={"username": "usr", "password": "notsosecret"})
    assert res.status_code == 201
    assert redis_client.hexists("users", "usr")

    # User alreay exist
    res = client.post("/account", json={"username": "usr", "password": "notsosecret"})
    assert res.status_code == 400


def test_login(client: FlaskClient, redis_client: FakeStrictRedis):
    res = client.post("/account", json={"username": "usr", "password": "notsosecret"})

    # No data
    res = client.post("/login")
    assert res.status_code == 400

    # Invalid username
    res = client.post("/login", json={"username": "noexist", "password": "notsosecret"})
    assert res.status_code == 400

    # Invalid password
    res = client.post("/login", json={"username": "usr", "password": "invalid"})
    assert res.status_code == 400

    # Proper login
    res = client.post("/login", json={"username": "usr", "password": "notsosecret"})
    assert res.status_code == 200

    # Check JWT token
    user_id = redis_client.hget("users", "usr")
    decoded_jwt = jwt.decode(
        res.get_json()["data"]["jwt"], os.environ["JWT_SECRET"], algorithms=["HS256"]
    )
    assert decoded_jwt["user_id"] == user_id
