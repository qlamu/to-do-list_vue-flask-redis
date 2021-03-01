import string
import random
from flask.testing import FlaskClient
from fakeredis import FakeStrictRedis
from typing import Union


def create_acc_and_login(client: FlaskClient, redis_client: FakeStrictRedis) -> Union[str, str]:
    username = "".join(random.choices(string.ascii_uppercase + string.digits, k=50))
    password = "".join(random.choices(string.ascii_uppercase + string.digits, k=50))

    res = client.post("/account", json={"username": username, "password": password})
    res = client.post("/login", json={"username": username, "password": password})
    auth_token = res.get_json()["data"]["jwt"]
    user_id = redis_client.hget("users", username)
    return user_id, auth_token
