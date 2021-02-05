from flask import Blueprint, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt

bp_auth = Blueprint("auth", __name__)


@bp_auth.route('/account', methods=['POST'])
def register():
    """
    [POST] Register a new user
        Expects: a 'application/json' request with the keys: 'username', 'password'
    """
    redis_client = current_app.config['redis_client']

    data = request.get_json()
    if((data is None) or ('username' not in data) or ('password' not in data)):
        return {'status': 400, 'message': "Expects a 'application/json' request with the keys: 'username', 'password'"}, 400

    if(redis_client.hexists('users', data['username'])):
        return {'status': 400, 'message': 'The user already exists'}, 400

    user_id = redis_client.incr('next_user_id', 1)
    redis_client.hset('users', mapping={data['username']: user_id})
    redis_client.hset('user:%d' % user_id, mapping={
                      'username': data['username'], 'password': generate_password_hash(data['password'])})

    return {'status': 201, 'message': 'User created'}, 201


@bp_auth.route('/login', methods=['POST'])
def login():
    """
    [POST] Login an existing user
        Expects: a 'application/json' request with the keys: 'username', 'password'
    """
    redis_client = current_app.config['redis_client']

    data = request.get_json()
    if((data is None) or ('username' not in data) or ('password' not in data)):
        return {'status': 400, 'message': "Expects a 'application/json' request with the keys: 'username', 'password'"}, 400

    user_id = redis_client.hget('users', data['username'])
    if(user_id is None):
        return {'status': 404, 'message': "User %s does not exist" % data['username']}, 404
    user_id = user_id.decode()

    user_pwhash = redis_client.hget('user:%s' % user_id, 'password')
    if(user_pwhash and not check_password_hash(user_pwhash.decode(), data['password'])):
        return {'status': 400, 'message': 'Invalid password'}, 400

    encoded_jwt = jwt.encode({'user_id': user_id},
                             os.environ['JWT_SECRET'], algorithm='HS256')

    return {'status': 200, 'message': 'Logged in', 'data': {'jwt': encoded_jwt}}, 200
