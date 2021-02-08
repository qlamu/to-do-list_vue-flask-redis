from flask import Blueprint, current_app, request

from api.utils import check_jwt_token

bp_todos = Blueprint("todos", __name__)


@bp_todos.route('/lists/todos/<id_list>', methods=['GET', 'PUT'])
@check_jwt_token
def todos(user_id, id_list):
    """
    [GET] Get existing todos from the list id_list
    [PUT] Add a new todo to the list id_list
        Expects: a 'application/json' request with the keys: 'description', 'is_done'
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    if(request.method == 'GET'):
        return "", 501

    if(request.method == 'PUT'):
        todo_id = redis_client.incr('next_todo_id', 1)
        return "", 501

    return "", 501


@bp_todos.route('/lists/todos/<id_list>/<id_todo>', methods=['GET', 'DELETE', 'PATCH'])
@check_jwt_token
def crud_todos(user_id, id_list, id_todo):
    """
    [GET]    Get the data for the todo id_todo located in the list id_list
    [DELETE] Delete the todo id_todo from the list id_list
    [PATCH]  Update the todo id_todo with new contents supplied in JSON
        Expects: a 'application/json' request with the keys: 'description', 'is_done'
    This endpoint require authentication
    """
    redis_client = current_app.config['redis_client']

    return "", 501
