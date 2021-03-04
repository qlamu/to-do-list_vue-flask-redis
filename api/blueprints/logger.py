import json
from flask import Blueprint, current_app, request
from marshmallow import ValidationError
from api.utils.schemas import LogSchema

bp_logger = Blueprint("logger", __name__)


@bp_logger.route("/log", methods=["GET", "POST"])
def logger():
    redis_client = current_app.config["redis_client"]

    if request.method == "GET":
        logs = [json.loads(log) for log in redis_client.lrange("logs", 0, -1)]

        return {"status": 200, "message": "OK, Logs queried", "data": {"logs": logs}}, 200

    if request.method == "POST":
        try:
            data = LogSchema().load(request.get_json())
        except ValidationError as err:
            return {"status": 400, "message": err.messages}, 400

        redis_client.lpush("logs", json.dumps(data))

        return {"status": 201, "message": "OK, Log created"}, 201
