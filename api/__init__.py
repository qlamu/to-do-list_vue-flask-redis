import os
import redis
import fakeredis
from flask import Flask, render_template

from api.blueprints.auth import bp_auth
from api.blueprints.lists import bp_lists
from api.blueprints.todos import bp_todos
from api.blueprints.logger import bp_logger


def create_app(testing=False):

    app = Flask(__name__)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_lists, url_prefix="/lists")
    app.register_blueprint(bp_todos, url_prefix="/lists/todos")
    app.register_blueprint(bp_logger, url_prefix="/logger")

    if testing:
        redis_client = fakeredis.FakeStrictRedis(decode_responses=True)
        app.testing = True
        app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
        os.environ["JWT_SECRET"] = "aHR0cHM6Ly9naXRodWIuY29tL3FsYW11L3RvLWRvLWx"
        os.environ["FLASK_ENV"] = "development"
    else:
        redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    app.config["redis_client"] = redis_client

    @app.route("/")
    @app.route("/doc")
    def index():
        return render_template("swaggerui.html")

    return app
