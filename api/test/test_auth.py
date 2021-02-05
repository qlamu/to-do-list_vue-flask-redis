import jwt
import os
from flask.testing import FlaskClient
from flask import Response 
from fakeredis import FakeStrictRedis


def test_register(client: FlaskClient, redis_client: FakeStrictRedis):
    # Empty request
    rv: Response = client.post('/account')
    assert rv.status_code == 400

    # No data
    rv = client.post('/account')
    assert rv.get_json()['message'] == "Expects a 'application/json' request with the keys: 'username', 'password'"

    # Proper data
    rv = client.post('/account', json={'username': 'usr', 'password': 'notsosecret'})
    assert rv.status_code == 201
    assert redis_client.hexists('users', 'usr')

    # User alreay exist
    rv = client.post('/account', json={'username': 'usr', 'password': 'notsosecret'})
    assert rv.get_json()['message'] == 'The user already exists'


def test_login(client: FlaskClient, redis_client: FakeStrictRedis):
    rv: Response = client.post('/account', json={'username': 'usr', 'password': 'notsosecret'})

    # No data
    rv = client.post('/login')
    assert rv.get_json()['message'] == "Expects a 'application/json' request with the keys: 'username', 'password'"

    # Invalid username
    rv = client.post('/login', json={'username': 'noexist', 'password': 'notsosecret'})
    assert rv.get_json()['message'] == 'User noexist does not exist'

    # Invalid password
    rv = client.post('/login', json={'username': 'usr', 'password': 'invalid'})
    assert rv.get_json()['message'] == 'Invalid password'

    # Proper login
    rv = client.post('/login', json={'username': 'usr', 'password': 'notsosecret'})
    assert rv.status_code == 200

    # Check JWT token
    user_id = redis_client.hget('users', 'usr').decode()
    decoded_jwt = jwt.decode(rv.get_json()['data']['jwt'], os.environ['JWT_SECRET'], algorithms=['HS256'])
    assert decoded_jwt['user_id'] == user_id