from flask import Blueprint, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
from marshmallow import ValidationError
from api.utils.schemas import AuthSchema

bp_auth = Blueprint("auth", __name__)


@bp_auth.route('/account', methods=['POST'])
def register():
    """
    [POST] Register a new user
        Expects: a 'application/json' request with the fields: 'username', 'password'
    """
    redis_client = current_app.config['redis_client']

    try:
        data = AuthSchema().load(request.get_json())
    except ValidationError as err:
        return {'status': 400, 'message': err.messages}, 400

    if(redis_client.hexists('users', data['username'])):
        return {'status': 400, 'message': 'The user already exists'}, 400

    user_id = redis_client.incr('next_user_id', 1)
    redis_client.hset('users', mapping={data['username']: user_id})
    redis_client.hset(f'user:{user_id}', mapping={
                      'username': data['username'], 'password': generate_password_hash(data['password'])})

    return {'status': 201, 'message': 'User created'}, 201


@bp_auth.route('/login', methods=['POST'])
def login():
    """
    [POST] Login an existing user
        Expects: a 'application/json' request with the fields: 'username', 'password'
    """
    redis_client = current_app.config['redis_client']

    try:
        data = AuthSchema().load(request.get_json())
    except ValidationError as err:
        return {'status': 400, 'message': err.messages}, 400

    user_id = redis_client.hget('users', data['username'])
    if(user_id is None):
        return {'status': 404, 'message': "User does not exist"}, 404

    user_pwhash = redis_client.hget(f'user:{user_id}', 'password')
    if(user_pwhash and not check_password_hash(user_pwhash, data['password'])):
        return {'status': 400, 'message': 'Invalid password'}, 400

    encoded_jwt = jwt.encode({'user_id': user_id},
                             os.environ['JWT_SECRET'], algorithm='HS256')

    return {'status': 200, 'message': 'Logged in', 'data': {'jwt': encoded_jwt}}, 200
