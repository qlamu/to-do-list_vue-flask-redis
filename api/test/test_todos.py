from flask.testing import FlaskClient
from flask import Response
from fakeredis import FakeStrictRedis
import string
import random


def login_and_create_list(client: FlaskClient, redis_client: FakeStrictRedis):
    username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))

    res = client.post('/account', json={'username': username, 'password': password})
    res = client.post('/login', json={'username': username, 'password': password})
    auth_token = res.get_json()['data']['jwt']

    res = client.put('/lists', headers={'Authorization': 'Bearer ' +
                                        auth_token}, json={'title': 'Test list'})

    return auth_token, res.get_json()['data']['list_id']


def test_authentication(client: FlaskClient):
    res: Response = client.get('/lists/todos/0')
    assert res.status_code == 401


def test_create_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo'})

    assert res.status_code == 201
    json = res.get_json()
    assert 'todo_id' in json['data']
    assert redis_client.scard('list_content:{}'.format(list_id)) == 1


def test_get_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    # Add todos
    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo'})
    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo2'})

    # Get all todos
    res = client.get('/lists/todos/{}'.format(list_id),
                     headers={'Authorization': 'Bearer ' + auth_token})
    assert res.status_code == 200
    json = res.get_json()
    assert 'data' in json
    assert len(json['data']) == 2
    assert 'description' in json['data'][0]
    assert 'is_done' in json['data'][0]
    assert 'todo_id' in json['data'][0]


def test_get_specific_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    # Add todos
    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo'})
    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo2'})
    todo_id = res.get_json()['data']['todo_id']

    res = client.get('/lists/todos/{}/{}'.format(list_id, todo_id),
                     headers={'Authorization': 'Bearer ' + auth_token})
    assert res.status_code == 200
    json = res.get_json()
    assert 'data' in json
    assert 'description' in json['data']
    assert 'is_done' in json['data']


def test_patch_specific_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    # Add todo
    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo'})
    todo_id = res.get_json()['data']['todo_id']

    res = client.patch('/lists/todos/{}/{}'.format(list_id, todo_id),
                       headers={'Authorization': 'Bearer ' + auth_token}, json={'is_done': 1})


def test_delete_specific_todo(client: FlaskClient, redis_client: FakeStrictRedis):
    auth_token, list_id = login_and_create_list(client, redis_client)

    # Add todos
    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo'})
    res = client.put('/lists/todos/{}'.format(list_id), headers={'Authorization': 'Bearer ' +
                                                                 auth_token}, json={'description': 'Test todo2'})
    todo_id = res.get_json()['data']['todo_id']

    # Delete todo
    res = client.delete('/lists/todos/{}/{}'.format(list_id, todo_id),
                        headers={'Authorization': 'Bearer ' + auth_token})
    assert res.status_code == 200

    # Get all todos
    res = client.get('/lists/todos/{}'.format(list_id),
                     headers={'Authorization': 'Bearer ' + auth_token})
    json = res.get_json()
    assert len(json['data']) == 1
