from flask import Blueprint, current_app, request
from api.utils import check_jwt_token

bp_lists = Blueprint("lists", __name__)


@bp_lists.route('/lists', methods=['GET', 'PUT'])
@check_jwt_token
def lists(user_id: str):
    """
    [GET] Get all the lists of the user
    [PUT] Add a new list for the user
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(request.method == 'GET'):
        lists = [redis_client.hgetall('list_infos:' + id).update({'list_id': id})
                 for id in redis_client.smembers('lists:' + user_id)]

        return {'status': 200, 'message': 'Success', 'data': {'lists': lists}}, 200

    if(request.method == 'PUT'):
        data = request.get_json()
        if((data is None) or ('title' not in data)):
            return {'status': 400, 'message': "Expects a 'application/json' request with the field: 'title'"}, 400

        list_id = redis_client.incr('next_list_id', 1)
        redis_client.sadd('lists:' + user_id, list_id)
        redis_client.hset('list_infos:%d' % list_id, 'title', data['title'])
        return {'status': 201, 'message': 'Created', 'data': {'list_id': list_id}}, 201

    return {'status': 400, 'message': 'Requests to /lists must be GET or PUT'}, 400


@bp_lists.route('/lists/<string:list_id>', methods=['GET', 'DELETE', 'PATCH'])
@check_jwt_token
def crud_lists(user_id: str, list_id: str):
    """
    CRUD operations on a list
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(not redis_client.sismember('lists:' + user_id, list_id)):
        return {'status': 403, 'message': 'Invalid owner for the list %s' % list_id}, 403

    if(request.method == 'GET'):
        return {'status': 200, 'message': 'Success', 'data': redis_client.hgetall('list_infos:' + list_id)}, 200

    if(request.method == 'DELETE'):
        [redis_client.delete('todo:' + id) for id in redis_client.smembers('list_content:' + list_id)]
        redis_client.delete('list_infos:' + list_id, 'list_content:' + list_id)
        redis_client.srem('lists:' + user_id, list_id)
        return {'status': 200, 'message': 'The list %s has been deleted' % list_id}, 200

    if(request.method == 'PATCH'):
        data = request.get_json()
        if((data is None) or ('title' not in data)):
            return {'status': 400, 'message': "Expects a 'application/json' request with the field: 'title'"}, 400

        redis_client.hset('list_infos:' + list_id, 'title', data['title'])
        return {'status': 200, 'message': 'List %s patched' % list_id}, 200
