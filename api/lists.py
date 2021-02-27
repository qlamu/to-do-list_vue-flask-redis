from flask import Blueprint, current_app, request
from marshmallow import ValidationError
from api.utils.decorators import check_jwt_token
from api.utils.schemas import ListSchema

bp_lists = Blueprint("lists", __name__)


@bp_lists.route('/lists', methods=['GET', 'PUT'])
@check_jwt_token
def lists(user_id: int):
    """
    [GET] Get all the lists of the user
    [PUT] Add a new list for the user
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(request.method == 'GET'):
        lists = [redis_client.hgetall('list_infos:{}'.format(id)) | {'list_id': id}
                 for id in redis_client.smembers('lists:{}'.format(user_id))]

        return {'status': 200, 'message': 'Success', 'data': {'lists': lists}}, 200

    if(request.method == 'PUT'):
        try:
            data = ListSchema().load(request.get_json())
        except ValidationError as err:
            return {'status': 400, 'message': err.messages}, 400

        list_id = redis_client.incr('next_list_id', 1)
        redis_client.sadd('lists:{}'.format(user_id), list_id)
        redis_client.hset('list_infos:{}'.format(list_id), 'title', data['title'])
        return {'status': 201, 'message': 'Created', 'data': {'list_id': list_id}}, 201

    return {'status': 405, 'message': 'Requests to /lists must be GET or PUT'}, 405


@bp_lists.route('/lists/<int:list_id>', methods=['GET', 'DELETE', 'PATCH'])
@check_jwt_token
def crud_lists(user_id: int, list_id: int):
    """
    CRUD operations on a list
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(not redis_client.sismember('lists:{}'.format(user_id), list_id)):
        return {'status': 403, 'message': 'Invalid owner for the selected list'}, 403

    if(request.method == 'GET'):
        return {'status': 200, 'message': 'Success', 'data': redis_client.hgetall('list_infos:{}'.format(list_id))}, 200

    if(request.method == 'DELETE'):
        [redis_client.delete('todo:{}'.format(id)) for id in redis_client.smembers('list_content:{}'.format(list_id))]
        redis_client.delete('list_infos:{}'.format(list_id), 'list_content:{}'.format(list_id))
        redis_client.srem('lists:{}'.format(user_id), list_id)
        return {'status': 200, 'message': 'The list has been deleted'}, 200

    if(request.method == 'PATCH'):
        try:
            data = ListSchema().load(request.get_json())
        except ValidationError as err:
            return {'status': 400, 'message': err.messages}, 400

        redis_client.hset('list_infos:{}'.format(list_id), 'title', data['title'])
        return {'status': 200, 'message': 'List patched'}, 200

    return {'status': 405, 'message': 'Requests to /lists/<id_list> must be GET, DELETE or PATCH'}, 405
