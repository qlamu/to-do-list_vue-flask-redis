from flask import Flask
from werkzeug.utils import redirect
import fakeredis
import redis
from dotenv import load_dotenv
from flasgger import Swagger

from api.blueprints.auth import bp_auth
from api.blueprints.lists import bp_lists
from api.blueprints.todos import bp_todos


def create_app(testing=False):
    load_dotenv()

    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Todos API',
        'version': 'v1',
        'description': 'API for a simple todo app, source: [https://github.com/qlamu/to-do-list_vue-flask-redis](https://github.com/qlamu/to-do-list_vue-flask-redis)',
        'termsOfService': '',
        'hide_top_bar': True,
    }

    Swagger(app)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_lists)
    app.register_blueprint(bp_todos)

    if(testing):
        redis_client = fakeredis.FakeStrictRedis(decode_responses=True)
        app.testing = True
    else:
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    app.config['redis_client'] = redis_client

    @app.route('/')
    @app.route('/help')
    def index(): return redirect('/apidocs')

    return app


if __name__ == "__main__":
    app = create_app(True)
    app.run()
