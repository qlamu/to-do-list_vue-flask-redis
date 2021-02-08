import os
import jwt
from functools import wraps
from flask import request


def check_jwt_token(f):
    """
    Check authentication with the supplied jwt token and add user_id to the parameters
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        if(authorization is None):
            return {'status': 403, 'message': 'No authorization token provided'}, 403
        encoded_jwt = authorization.removeprefix('Bearer ')

        try:
            data = jwt.decode(
                encoded_jwt, os.environ['JWT_SECRET'], algorithms=['HS256'])
            user_id = data['user_id']
        except:
            return {'status': 403, 'message': 'JWT token invalid'}, 403

        return f(user_id, *args, **kwargs)
    return decorator
