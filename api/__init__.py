from flask import Flask, render_template
from dotenv import load_dotenv
import fakeredis
import redis

from api.blueprints.auth import bp_auth
from api.blueprints.lists import bp_lists
from api.blueprints.todos import bp_todos


def create_app(testing=False):
    load_dotenv()

    app = Flask(__name__)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_lists)
    app.register_blueprint(bp_todos)

    if(testing):
        redis_client = fakeredis.FakeStrictRedis(decode_responses=True)
        app.testing = True
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    else:
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    app.config['redis_client'] = redis_client

    @app.route('/')
    @app.route('/apidocs')
    def index(): 
        return render_template('swaggerui.html')

    return app


if __name__ == "__main__":
    app = create_app(True)
    app.run()