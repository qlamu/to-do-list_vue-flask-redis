from flask import Blueprint, current_app, request

from api.utils import check_jwt_token

bp_todos = Blueprint("todos", __name__)


@bp_todos.route('/lists/todos/<string:list_id>', methods=['GET', 'PUT'])
@check_jwt_token
def todos(user_id: str, list_id: str):
    """
    [GET] Get existing todos from the list list_id
    [PUT] Add a new todo to the list list_id
        Expects: a 'application/json' request with the fields: 'description', 'is_done'
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(not redis_client.sismember('lists:' + user_id, list_id)):
        return {'status': 403, 'message': 'Invalid owner for the list %s' % list_id}, 401

    if(request.method == 'GET'):
        todos = [redis_client.hgetall('todo:' + id) | {'todo_id': id} for id in redis_client.smembers('list:' + list_id)]
        return {'status': 200, 'message': 'Todos access authorized', 'data': todos}, 200

    if(request.method == 'PUT'):
        data = request.get_json()
        if((data is None) or ('description' not in data)):
            return {'status': 400, 'message': "Expects a 'application/json' request with the field: 'todo'"}, 400

        new_todo_id = redis_client.incr('next_todo_id', 1)
        redis_client.sadd('list:' + list_id, new_todo_id)
        redis_client.hset('todo:%d' % new_todo_id,
                          mapping={'description': data['description'], 'is_done': 0})

        return {'status': 201, 'message': 'Todo created succesfully'}, 201

    return {'status': 405, 'message': 'Requests to /lists/todos/<list_id> must be GET or PUT'}, 405


@bp_todos.route('/lists/todos/<string:list_id>/<string:todo_id>', methods=['GET', 'DELETE', 'PATCH'])
@check_jwt_token
def crud_todos(user_id: str, list_id: str, todo_id: str):
    """
    [GET]    Get the data for the todo todo_id located in the list list_id
    [DELETE] Delete the todo todo_id from the list list_id
    [PATCH]  Update the todo todo_id with new contents supplied in JSON
        Expects: a 'application/json' request with the fields: 'description', 'is_done'
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(not (redis_client.sismember('lists:' + user_id, list_id) and redis_client.sismember('list:' + list_id, todo_id))):
        return {'status': 403, 'message': 'Invalid owner for the list %s or Todo %s does not exist' % (list_id, todo_id)}, 401

    if(request.method == 'GET'):
        return {'status': 200, 'message': 'Success', 'data': redis_client.hgetall('todo:' + todo_id)}, 200

    if(request.method == 'DELETE'):
        isDeleted = redis_client.delete('todo:' + todo_id)
        if(isDeleted):
            return {'status': 200 , 'message': 'Todo %s deleted' % todo_id}, 200
        return {'status': 400, 'message': 'Todo %s does not exist' % todo_id}, 400

    if(request.method == 'PATCH'):
        data = request.get_json()
        if((data is None) or ('description' not in data or 'is_done' not in data)):
            return {'status': 400, 'message': "Expects a 'application/json' request with the field: 'description' or 'is_done', or both"}, 400

        new_mapping: dict = {}
        if('description' in data): new_mapping['description'] = data['description']
        if('is_done' in data):

            new_mapping['is_done'] = data['is_done']
        redis_client.hset('todo:' + todo_id, mapping=new_mapping)

        return {'status': 200 , 'message': 'Todo %s patched' % todo_id}, 200

    return {'status': 405, 'message': 'Requests to /lists/todos/<list_id>/<todo_id> must be GET, DELETE or PATCH'}, 405
