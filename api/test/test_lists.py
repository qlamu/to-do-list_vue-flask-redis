from flask.testing import FlaskClient
from flask import Response 
from fakeredis import FakeStrictRedis


def test_add_list(client: FlaskClient, redis_client: FakeStrictRedis):
    # Not authenticated
    rv: Response = client.get('/lists')
    assert rv.status_code == 403

    # Create account and login
    rv = client.post('/account', json={'username': 'usr', 'password': 'notsosecret'})
    rv = client.post('/login', json={'username': 'usr', 'password': 'notsosecret'})
    auth_token = rv.get_json()['data']['jwt']

    # Check the user doesn't have any lists
    rv = client.get('/lists', headers={'Authorization': 'Bearer ' + auth_token})
    assert rv.status_code == 200
    json = rv.get_json()
    assert ('data' in json) and ('lists' in json['data'])
    assert len(json['data']['lists']) == 0
    user_id = redis_client.hget('users', 'usr').decode()
    assert not redis_client.exists('lists:' + user_id)

    # Add data
    rv = client.put('/lists', headers={'Authorization': 'Bearer ' + auth_token})
    assert rv.status_code == 201
    assert redis_client.llen('lists:' + user_id) == 1

    # Get new data
    rv = client.get('/lists', headers={'Authorization': 'Bearer ' + auth_token})
    assert rv.status_code == 200
    assert ('data' in json) and ('lists' in json['data'])
    assert len(json['data']['lists']) == 1
    