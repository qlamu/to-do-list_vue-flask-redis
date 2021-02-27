import os
import jwt
from functools import wraps
from flask import request, current_app


def check_jwt_token(f):
    """
    Check authentication with the supplied jwt token and add user_id to the parameters
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        if(authorization is None):
            return {'status': 401, 'message': 'No authorization token provided'}, 401
        encoded_jwt = authorization.removeprefix('Bearer ')

        try:
            data = jwt.decode(
                encoded_jwt, os.environ['JWT_SECRET'], algorithms=['HS256'])
            user_id = data['user_id']
        except:
            return {'status': 401, 'message': 'JWT token invalid'}, 401

        if(not current_app.config['redis_client'].exists(f'user:{user_id}')):
            return {'status': 401, 'message': 'JWT token references unknown user'}, 401

        return f(user_id, *args, **kwargs)
    return decorator
