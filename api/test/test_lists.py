from flask.testing import FlaskClient
from fakeredis import FakeStrictRedis
from api.test.utils import create_acc_and_login


def test_authentication(client: FlaskClient):
    res = client.get("/lists")
    assert res.status_code == 401

    res = client.put("/lists/123")
    assert res.status_code == 405


def test_get_lists(client: FlaskClient, redis_client: FakeStrictRedis):
    user_id, auth_token = create_acc_and_login(client, redis_client)

    assert redis_client.scard("lists:" + user_id) == 0

    # Add a list directly in the database
    list_id = redis_client.incr("next_list_id", 1)
    redis_client.sadd("lists:" + user_id, list_id)

    # Check updated lists
    res = client.get("/lists", headers={"Authorization": "Bearer " + auth_token})
    assert res.status_code == 200
    json = res.get_json()

    assert ("data" in json) and ("lists" in json["data"])
    assert len(json["data"]["lists"]) == 1


def test_put_list(client: FlaskClient, redis_client: FakeStrictRedis):
    user_id, auth_token = create_acc_and_login(client, redis_client)

    assert redis_client.scard("lists:" + user_id) == 0

    # Add data
    res = client.put(
        "/lists",
        headers={"Authorization": "Bearer " + auth_token},
        json={"title": "Test list"},
    )
    assert res.status_code == 201
    assert redis_client.scard("lists:" + user_id) == 1

    json = res.get_json()
    assert "data" in json
    assert "list_id" in json["data"]

    list_id = json["data"]["list_id"]
    assert redis_client.exists(f"list_infos:{list_id}") == 1


def test_get_specific_list(client: FlaskClient, redis_client: FakeStrictRedis):
    _, auth_token = create_acc_and_login(client, redis_client)

    # Create a new list
    res = client.put(
        "/lists",
        headers={"Authorization": "Bearer " + auth_token},
        json={"title": "Test list"},
    )
    list_id = res.get_json()["data"]["list_id"]

    # Get the newly added list
    res = client.get(f"/lists/{list_id}", headers={"Authorization": "Bearer " + auth_token})
    assert res.status_code == 200

    json = res.get_json()
    assert "data" in json
    assert "title" in json["data"]
    assert json["data"]["title"] == "Test list"


def test_patch_specific_list(client: FlaskClient, redis_client: FakeStrictRedis):
    _, auth_token = create_acc_and_login(client, redis_client)

    # Create a new list
    res = client.put(
        "/lists",
        headers={"Authorization": "Bearer " + auth_token},
        json={"title": "Test list"},
    )
    list_id = res.get_json()["data"]["list_id"]

    # Patch it
    res = client.patch(
        f"/lists/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"title": "New Name"},
    )
    assert res.status_code == 200

    # Get it and check the new title
    res = client.get(f"/lists/{list_id}", headers={"Authorization": "Bearer " + auth_token})
    json = res.get_json()
    assert "data" in json
    assert "title" in json["data"]
    assert json["data"]["title"] == "New Name"


def test_delete_specific_list(client: FlaskClient, redis_client: FakeStrictRedis):
    user_id, auth_token = create_acc_and_login(client, redis_client)

    # Create a new list
    res = client.put(
        "/lists",
        headers={"Authorization": "Bearer " + auth_token},
        json={"title": "Test list"},
    )
    list_id = res.get_json()["data"]["list_id"]

    # Delete it
    res = client.delete(f"/lists/{list_id}", headers={"Authorization": "Bearer " + auth_token})
    assert res.status_code == 200
    assert not redis_client.sismember("lists:" + user_id, list_id)
    assert not redis_client.exists(f"list_infos:{list_id}")
    assert not redis_client.exists(f"list_content:{list_id}")


def test_access_specific_list(client: FlaskClient, redis_client: FakeStrictRedis):
    _, auth_token_1 = create_acc_and_login(client, redis_client)
    _, auth_token_2 = create_acc_and_login(client, redis_client)

    # Create a list with user_1
    res = client.put(
        "/lists",
        headers={"Authorization": "Bearer " + auth_token_1},
        json={"title": "Test list"},
    )
    list_id = res.get_json()["data"]["list_id"]

    # Try to access it with user_2
    res = client.get(f"/lists/{list_id}", headers={"Authorization": "Bearer " + auth_token_2})
    assert res.status_code == 403
