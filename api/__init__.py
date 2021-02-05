import os
from flask import Flask, request
from werkzeug.utils import redirect
import fakeredis
import jwt
import redis
from dotenv import load_dotenv
from functools import wraps
import json

from api.auth import bp_auth


def create_app(testing=False):
    load_dotenv()

    app = Flask(__name__)
    app.register_blueprint(bp_auth)

    if(testing):
        redis_client = fakeredis.FakeStrictRedis()
        app.testing = True
    else:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
    app.config['redis_client'] = redis_client

    @app.route('/')
    def index():
        return redirect('/help')

    @app.route('/help')
    def help():
        """Print available routes"""
        func_list = {}
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
        return func_list

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

    @app.route('/lists', methods=['GET', 'PUT'])
    @check_jwt_token
    def lists(user_id):
        """
        [GET] Get all the lists of the user
        [PUT] Add a new list for the user
            Expects: a 'application/json' request with the keys:
        This endpoint require authentication
        """

        if(request.method == 'GET'):
            lists = redis_client.lrange('lists:' + user_id, 0, -1)
            return {'status': 200, 'message': 'Success', 'data': {'lists': json.dumps(lists)}}, 200

        if(request.method == 'PUT'):
            list_id = redis_client.incr('next_list_id', 1)
            redis_client.lpush('lists:' + user_id, list_id)
            return {'status': 201, 'message': 'Created'}, 201

        return {'status': 400, 'message': 'Requests to /lists must be GET or PUT'}, 400

    @app.route('/lists/<id_list>', methods=['GET', 'DELETE', 'PATCH'])
    @check_jwt_token
    def crud_lists(user_id, id_list):
        """
        CRUD operations on a list
        This endpoint require authentication
        """
        # CHECK AUTH HERE
        if(redis_client.exist(id_list) == 0):
            return {'status': 404, 'message': 'The list {id_list} does not exist'.format(id_list)}, 404

        if(request.method == 'GET'):
            return "", 501

        if(request.method == 'DELETE'):
            return "", 501

        if(request.method == 'PATCH'):
            return "", 501

    @app.route('/lists/todos/<id_list>', methods=['GET', 'PUT'])
    @check_jwt_token
    def todos(user_id, id_list):
        """
        [GET] Get existing todos from the list id_list
        [PUT] Add a new todo to the list id_list
            Expects: a 'application/json' request with the keys: 'description', 'is_done'
        This endpoint require authentication
        """
        # CHECK AUTH HERE

        if(request.method == 'GET'):
            return "", 501

        if(request.method == 'PUT'):
            todo_id = redis_client.incr('next_todo_id', 1)
            return "", 501

        return "", 501

    @app.route('/lists/todos/<id_list>/<id_todo>', methods=['GET', 'DELETE', 'PATCH'])
    @check_jwt_token
    def crud_todos(user_id, id_list, id_todo):
        """
        [GET]    Get the data for the todo id_todo located in the list id_list
        [DELETE] Delete the todo id_todo from the list id_list
        [PATCH]  Update the todo id_todo with new contents supplied in JSON
            Expects: a 'application/json' request with the keys: 'description', 'is_done'
        This endpoint require authentication
        """
        # CHECK AUTH HERE
        return "", 501

    @app.route('/logger/log', methods=['POST'])
    def add_log():
        """
        [POST] Add a new log
            Expects: a 'application/json' request with the keys:
                'username': the user who realized the action,
                'status': one of FAIL, WARNING, SUCCESS,
                'message': description of the performed action
        """
        return "", 501

    @app.route('/logger/log')
    def get_logs():
        """
        [GET] Get all the logs from the database
        """
        return "", 501

    return app
