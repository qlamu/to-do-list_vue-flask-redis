from flask.testing import FlaskClient
from fakeredis import FakeStrictRedis
from api.test.utils import create_acc_and_login


def test_add_log(client: FlaskClient, redis_client: FakeStrictRedis):
    user_id, auth_token = create_acc_and_login(client, redis_client)

    username = redis_client.hget(f'user:{user_id}', 'username')

    # Invalid Schema
    res = client.post('/logger/log', headers={'Authorization': 'Bearer ' + auth_token},
                      json={'username': username, 'status': 'fail', 'message': 'nothing to worry'})
    assert res.status_code == 400

    # Connected user is not the same as the field username
    res = client.post('/logger/log', headers={'Authorization': 'Bearer ' + auth_token},
                      json={'username': 'not this one', 'status': 'FAIL', 'message': 'nothing to worry'})
    assert res.status_code == 403

    # Proper request
    res = client.post('/logger/log', headers={'Authorization': 'Bearer ' + auth_token},
                      json={'username': username, 'status': 'FAIL', 'message': 'nothing to worry'})
    assert res.status_code == 201
    assert redis_client.zcard('logs') == 1


def test_get_logs(client: FlaskClient, redis_client: FakeStrictRedis):
    user_id, auth_token = create_acc_and_login(client, redis_client)
    username = redis_client.hget(f'user:{user_id}', 'username')

    res = client.get('/logger/log', headers={'Authorization': 'Bearer ' + auth_token})
    json = res.get_json()
    assert res.status_code == 200
    assert 'data' in json
    assert 'logs' in json['data']
    assert len(json['data']['logs']) == 0

    res = client.post('/logger/log', headers={'Authorization': 'Bearer ' + auth_token},
                      json={'username': username, 'status': 'FAIL', 'message': 'nothing to worry'})

    res = client.get('/logger/log', headers={'Authorization': 'Bearer ' + auth_token})
    json = res.get_json()
    assert len(json['data']['logs']) == 1
