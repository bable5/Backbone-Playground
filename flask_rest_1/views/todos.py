from flask import Flask, jsonify, abort
from flask import make_response
from flask import request
from flask import url_for
from flask_rest_1 import app

def _make_todo(todo_id, title, order, done=False):
    return {
        'id': todo_id,
        'title': title,
        'order': order,
        'done': done
    }

def _v1_route(pattern):
    v1Route = '/todos/api/v1.0'
    return v1Route + pattern

def _make_public_todo(todo):
    print("TODO: " + str(todo))
    new_todo = {}
    for field in todo:
        if field == 'id':
            new_todo['uri'] = url_for('get_todo', todo_id=1, _external=True)
            new_todo['id'] = todo[field]
        else:
            new_todo[field] = todo[field]
    return new_todo

_todos = {
    1: _make_todo(1, "Make a flask server", 1, False)
    }

def _find_todo(todo_id):
    return [todo for todo in _todos if todo['id'] == todo_id]

def _set_todo(todo_id, todo):
    _todos[todo_id] = todo

def _create_todo_from_request(todo_id):
    return  _make_todo(
               todo_id = todo_id,
               title = request.json['title'],
               order = request.json['order'],
               done = request.json['done']
            )

def _delete_todo(todo_id):
    return _todos.pop(todo_id, None)

@app.route(_v1_route('/todos'))
def get_todos():
    return jsonify({'todos': [_make_public_todo(todo) for todo in _todos.values()]})

@app.route(_v1_route('/todos/<int:todo_id>'), methods=['GET'])
def get_todo(todo_id):
    todo = _find_todo(todo_id)
    if len(todo) == 0:
        abort(404)
    return jsonify({'todo': _make_public_todo(todo[0])})

@app.route(_v1_route('/todos/<int:todo_id>'), methods=['PUT'])
def put_todo(todo_id):
    if not request.json or not 'title' in request.json:
        abort(400)

    todo = _create_todo_from_request(todo_id)

    _set_todo(todo_id, todo)

    return make_response("", 204)

@app.route(_v1_route('/todos'), methods=['POST'])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)

    todo_id = max(_todos.keys) + 1
    todo = _create_todo_from_request(todo_id)
    _set_todo(todo_id, todo)

    return make_response(jsonify({'todo': todo}), 201)


@app.route(_v1_route('/todos/<int:todo_id>'), methods=['DELETE'])
def delete_todo(todo_id):
    todo = _delete_todo(todo_id)
    if None == todo:
        abort(404)
    else:
        return make_response("", 204)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

