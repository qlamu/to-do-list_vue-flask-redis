from flask.testing import FlaskClient
from flask import Response
from fakeredis import FakeStrictRedis


def test_authentication(client: FlaskClient):
    res: Response = client.get('/lists')
    assert res.status_code == 403

    res = client.put('/lists')
    assert res.status_code == 403


def test_get_list(client: FlaskClient, redis_client: FakeStrictRedis):
    # Create account and login
    res = client.post('/account', json={'username': 'usr', 'password': 'notsosecret'})
    res = client.post('/login', json={'username': 'usr', 'password': 'notsosecret'})
    auth_token = res.get_json()['data']['jwt']
    user_id = redis_client.hget('users', 'usr').decode()

    assert redis_client.llen('lists:' + user_id) == 0

    # Add a list directly in the database
    list_id = redis_client.incr('next_list_id', 1)
    redis_client.lpush('lists:' + user_id, list_id)

    # Check updated lists
    res = client.get('/lists', headers={'Authorization': 'Bearer ' + auth_token})
    assert res.status_code == 200
    json = res.get_json()
    assert ('data' in json) and ('lists' in json['data'])
    assert len(json['data']['lists']) == 1


def test_add_list(client: FlaskClient, redis_client: FakeStrictRedis):
    # Create account and login
    res = client.post('/account', json={'username': 'usr', 'password': 'notsosecret'})
    res = client.post('/login', json={'username': 'usr', 'password': 'notsosecret'})
    auth_token = res.get_json()['data']['jwt']
    user_id = redis_client.hget('users', 'usr').decode()

    assert redis_client.llen('lists:' + user_id) == 0

    # Add data
    res = client.put('/lists', headers={'Authorization': 'Bearer ' + auth_token})
    assert res.status_code == 201
    assert redis_client.llen('lists:' + user_id) == 1