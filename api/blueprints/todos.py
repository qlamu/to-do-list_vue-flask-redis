from flask import Blueprint, current_app, request
from marshmallow import ValidationError
from api.utils.decorators import check_jwt_token
from api.utils.schemas import AddTodoSchema, UpdateTodoSchema
bp_todos = Blueprint("todos", __name__)


@bp_todos.route('/<int:list_id>', methods=['GET', 'PUT'])
@check_jwt_token
def todos(user_id: int, list_id: int):
    """
    [GET] Get existing todos from the list list_id
    [PUT] Add a new todo to the list list_id
        Expects: a 'application/json' request with the fields: 'description', 'is_done'
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(not redis_client.sismember(f'lists:{user_id}', list_id)):
        return {'status': 403, 'message': 'Invalid owner for the selected list'}, 401

    if(request.method == 'GET'):
        todos = [redis_client.hgetall(f'todo:{id}') | {'todo_id': id} for id in redis_client.smembers(f'list_content:{list_id}')]
        return {'status': 200, 'message': 'Todos access authorized', 'data': todos}, 200

    if(request.method == 'PUT'):
        try:
            data = AddTodoSchema().load(request.get_json())
        except ValidationError as err:
            return {'status': 400, 'message': err.messages}, 400

        new_todo_id = redis_client.incr('next_todo_id', 1)
        redis_client.sadd(f'list_content:{list_id}', new_todo_id)
        redis_client.hset(f'todo:{new_todo_id}',
                          mapping={'description': data['description'], 'is_done': 0})

        return {'status': 201, 'message': 'Todo created succesfully', 'data': { 'todo_id': new_todo_id }}, 201

    return {'status': 405, 'message': 'Requests to /lists/todos/<list_id> must be GET or PUT'}, 405


@bp_todos.route('/<int:list_id>/<int:todo_id>', methods=['GET', 'DELETE', 'PATCH'])
@check_jwt_token
def crud_todos(user_id: int, list_id: int, todo_id: int):
    """
    [GET]    Get the data for the todo todo_id located in the list list_id
    [DELETE] Delete the todo todo_id from the list list_id
    [PATCH]  Update the todo todo_id with new contents supplied in JSON
        Expects: a 'application/json' request with the fields: 'description', 'is_done'
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(not (redis_client.sismember(f'lists:{user_id}', list_id) and redis_client.sismember(f'list_content:{list_id}', todo_id))):
        return {'status': 403, 'message': 'Invalid owner for the selected list or Todo does not exist'}, 401

    if(request.method == 'GET'):
        return {'status': 200, 'message': 'Success', 'data': redis_client.hgetall(f'todo:{todo_id}')}, 200

    if(request.method == 'DELETE'):
        redis_client.delete(f'todo:{todo_id}')
        redis_client.srem(f'list_content:{list_id}', todo_id)
        return {'status': 200 , 'message': 'Todo deleted'}, 200

    if(request.method == 'PATCH'):
        try:
            data = UpdateTodoSchema().load(request.get_json())
        except ValidationError as err:
            return {'status': 400, 'message': err.messages}, 400

        new_mapping: dict = {}
        if('description' in data): new_mapping['description'] = data['description']
        if('is_done' in data): new_mapping['is_done'] = data['is_done']
        redis_client.hset(f'todo:{todo_id}', mapping=new_mapping)

        return {'status': 200 , 'message': 'Todo patched'}, 200

    return {'status': 405, 'message': 'Requests to /lists/todos/<list_id>/<todo_id> must be GET, DELETE or PATCH'}, 405
