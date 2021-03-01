import pytest
from flask import Flask

from api import create_app


@pytest.fixture
def app():
    app = create_app(testing=True)
    yield app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def redis_client(app: Flask):
    return app.config["redis_client"]
