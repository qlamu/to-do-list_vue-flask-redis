import json
import time
import math
from flask import Blueprint, current_app, request
from marshmallow import ValidationError
from api.utils.schemas import LogSchema
from api.utils.decorators import check_jwt_token

bp_logger = Blueprint("logger", __name__)


@bp_logger.route("/log", methods=["GET", "POST"])
@check_jwt_token
def logger(user_id: str):
    redis_client = current_app.config["redis_client"]

    if request.method == "GET":
        logs = [
            json.loads(log) for log in redis_client.zrevrangebyscore("logs", math.inf, -math.inf)
        ]

        return {"status": 200, "message": "OK", "data": {"logs": logs}}, 200

    if request.method == "POST":
        try:
            data = LogSchema().load(request.get_json())
        except ValidationError as err:
            return {"status": 400, "message": err.messages}, 400

        user_id_from = redis_client.hget("users", data["username"])
        if user_id_from != user_id:
            return {
                "status": 403,
                "message": "Adding logs for other users is forbidden",
            }, 403

        redis_client.zadd("logs", mapping={json.dumps(data): time.time()})

        return {"status": 201, "message": "Created"}, 201
