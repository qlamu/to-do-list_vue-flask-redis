from flask import Blueprint, current_app, request

from api.utils import check_jwt_token

bp_lists = Blueprint("lists", __name__)


@bp_lists.route('/lists', methods=['GET', 'PUT'])
@check_jwt_token
def lists(user_id):
    """
    [GET] Get all the lists of the user
    [PUT] Add a new list for the user
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']


    if(request.method == 'GET'):
        lists = redis_client.lrange('lists:' + user_id, 0, -1)
        return {'status': 200, 'message': 'Success', 'data': {'lists': lists}}, 200

    if(request.method == 'PUT'):
        list_id = redis_client.incr('next_list_id', 1)
        redis_client.lpush('lists:' + user_id, list_id)
        return {'status': 201, 'message': 'Created'}, 201

    return {'status': 400, 'message': 'Requests to /lists must be GET or PUT'}, 400


@bp_lists.route('/lists/<id_list>', methods=['GET', 'DELETE', 'PATCH'])
@check_jwt_token
def crud_lists(user_id, id_list):
    """
    CRUD operations on a list
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(redis_client.exist(id_list) == 0):
        return {'status': 404, 'message': 'The list {id_list} does not exist'.format(id_list)}, 404

    if(request.method == 'GET'):
        return "", 501

    if(request.method == 'DELETE'):
        return "", 501

    if(request.method == 'PATCH'):
        return "", 501
