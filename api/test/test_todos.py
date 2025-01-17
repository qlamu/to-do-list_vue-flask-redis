from flask.testing import FlaskClient
from fakeredis import FakeStrictRedis
from api.test.utils import create_acc_and_login


def login_and_create_list(client: FlaskClient, redis_client: FakeStrictRedis):
    _, auth_token = create_acc_and_login(client, redis_client)

    res = client.put(
        "/lists",
        headers={"Authorization": "Bearer " + auth_token},
        json={"title": "Test list"},
    )

    return auth_token, res.get_json()["data"]["list_id"]


def test_authentication(client: FlaskClient):
    res = client.get("/lists/todos/0")
    assert res.status_code == 401


def test_create_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo"},
    )

    assert res.status_code == 201
    json = res.get_json()
    assert "todo_id" in json["data"]
    assert redis_client.scard(f"list_content:{list_id}") == 1


def test_get_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    # Add todos
    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo"},
    )
    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo2"},
    )

    # Get all todos
    res = client.get(f"/lists/todos/{list_id}", headers={"Authorization": "Bearer " + auth_token})
    assert res.status_code == 200
    json = res.get_json()
    assert "data" in json
    assert "todos" in json["data"]
    assert len(json["data"]["todos"]) == 2
    assert "description" in json["data"]["todos"][0]
    assert "is_done" in json["data"]["todos"][0]
    assert "todo_id" in json["data"]["todos"][0]


def test_get_specific_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo"},
    )
    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo2"},
    )
    todo_id = res.get_json()["data"]["todo_id"]

    res = client.get(
        f"/lists/todos/{list_id}/{todo_id}",
        headers={"Authorization": "Bearer " + auth_token},
    )
    assert res.status_code == 200
    json = res.get_json()
    assert "data" in json
    assert "todo" in json["data"]
    assert "description" in json["data"]["todo"]
    assert "is_done" in json["data"]["todo"]


def test_patch_specific_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    # Add todo
    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo"},
    )
    todo_id = res.get_json()["data"]["todo_id"]

    res = client.patch(
        f"/lists/todos/{list_id}/{todo_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"is_done": 1},
    )


def test_delete_specific_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    # Add todos
    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo"},
    )
    res = client.put(
        f"/lists/todos/{list_id}",
        headers={"Authorization": "Bearer " + auth_token},
        json={"description": "Test todo2"},
    )
    todo_id = res.get_json()["data"]["todo_id"]

    # Delete todo
    res = client.delete(
        f"/lists/todos/{list_id}/{todo_id}",
        headers={"Authorization": "Bearer " + auth_token},
    )
    assert res.status_code == 200

    # Get all todos
    res = client.get(f"/lists/todos/{list_id}", headers={"Authorization": "Bearer " + auth_token})
    json = res.get_json()
    assert len(json["data"]) == 1
