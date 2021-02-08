import os
from flask import Flask, request
from werkzeug.utils import redirect
import fakeredis

import redis
from dotenv import load_dotenv
from functools import wraps

from api.auth import bp_auth
from api.lists import bp_lists
from api.todos import bp_todos


def create_app(testing=False):
    load_dotenv()

    app = Flask(__name__)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_lists)
    app.register_blueprint(bp_todos)

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
