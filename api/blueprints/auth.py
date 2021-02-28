from flask import Blueprint, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
from marshmallow import ValidationError
from api.utils.schemas import AuthSchema

bp_auth = Blueprint("auth", __name__)


@bp_auth.route('/account', methods=['POST'])
def register():
    """Create a new user
    ---
    tags:
      - "Authentication"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: "#/definitions/AuthSchema"
    definitions:
      AuthSchema:
        type: object
        required:
        - username
        - password
        properties:
          username:
            type: string
            example: John Doe
          password:
            type: string
            example: h4sh3dp4ss
    responses:
      201:
        description: User created
      400:
        description: The user already exists or the supplied JSON is not formatted properly.
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
    """Login and receive a JWT Token
    Generate a unique JWT token corresponding to a user if the login is successful, the token is needed for most of the API routes.
    ---
    tags:
      - "Authentication"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: "#/definitions/AuthSchema"
    responses:
      200:
        description: Return a unique JWT associated to the user.
        schema:
          type: object
          properties:
            status: 
              type: integer
              example: 200
            message:
              type: string
              example: Logged in
            data:
              type: object
              properties:
                jwt: 
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
      400:
        description: User does not exist, the password is invalid or the supplied JSON is not formatted properly.
    """
    redis_client = current_app.config['redis_client']

    try:
        data = AuthSchema().load(request.get_json())
    except ValidationError as err:
        return {'status': 400, 'message': err.messages}, 400

    user_id = redis_client.hget('users', data['username'])
    if(user_id is None):
        return {'status': 400, 'message': "User does not exist, or the password is invalid"}, 400

    user_pwhash = redis_client.hget(f'user:{user_id}', 'password')
    if(user_pwhash and not check_password_hash(user_pwhash, data['password'])):
        return {'status': 400, 'message': 'User does not exist, or the password is invalid'}, 400

    encoded_jwt = jwt.encode({'user_id': user_id},
                             os.environ['JWT_SECRET'], algorithm='HS256')

    return {'status': 200, 'message': 'Logged in', 'data': {'jwt': encoded_jwt}}, 200
