from flask import Blueprint, current_app, request
from marshmallow import ValidationError
from api.utils.decorators import check_jwt_token, log_it
from api.utils.schemas import ListSchema

bp_lists = Blueprint("lists", __name__)


@bp_lists.route("", methods=["GET", "PUT"])
@log_it
@check_jwt_token
def lists(user_id: int):
    """
    [GET] Get all the lists of the user
    [PUT] Add a new list for the user
    This endpoint require authentication
    """
    redis_client = current_app.config["redis_client"]

    if request.method == "GET":
        lists = [
            redis_client.hgetall(f"list_infos:{id}") | {"list_id": id}
            for id in redis_client.smembers(f"lists:{user_id}")
        ]

        return {"status": 200, "message": "OK, Lists queried", "data": {"lists": lists}}, 200

    if request.method == "PUT":
        try:
            data = ListSchema().load(request.get_json())
        except ValidationError as err:
            return {"status": 400, "message": err.messages}, 400

        list_id = redis_client.incr("next_list_id", 1)
        redis_client.sadd(f"lists:{user_id}", list_id)
        redis_client.hset(f"list_infos:{list_id}", "title", data["title"])
        return {"status": 201, "message": "OK, List created", "data": {"list_id": list_id}}, 201

    return {"status": 405, "message": "Requests to /lists must be GET or PUT"}, 405


@bp_lists.route("/<int:list_id>", methods=["GET", "DELETE", "PATCH"])
@log_it
@check_jwt_token
def crud_lists(user_id: int, list_id: int):
    """
    CRUD operations on a list
    This endpoint require authentication
    """
    redis_client = current_app.config["redis_client"]

    if not redis_client.sismember(f"lists:{user_id}", list_id):
        return {"status": 403, "message": "Invalid owner for the selected list"}, 403

    if request.method == "GET":
        return {
            "status": 200,
            "message": "OK, List queried",
            "data": {"list": redis_client.hgetall(f"list_infos:{list_id}") | {"list_id": list_id}},
        }, 200

    if request.method == "DELETE":
        [
            redis_client.delete(f"todo:{id}")
            for id in redis_client.smembers(f"list_content:{list_id}")
        ]
        redis_client.delete(f"list_infos:{list_id}", f"list_content:{list_id}")
        redis_client.srem(f"lists:{user_id}", list_id)
        return {"status": 200, "message": "OK, List deleted"}, 200

    if request.method == "PATCH":
        try:
            data = ListSchema().load(request.get_json())
        except ValidationError as err:
            return {"status": 400, "message": err.messages}, 400

        redis_client.hset(f"list_infos:{list_id}", "title", data["title"])
        return {"status": 200, "message": "OK, List patched"}, 200

    return {
        "status": 405,
        "message": "Requests to /lists/<id_list> must be GET, DELETE or PATCH",
    }, 405
