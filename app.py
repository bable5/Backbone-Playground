#!/usr/bin/env python
from flask import Flask, jsonify, abort
from flask import make_response
from flask import request
from flask import url_for

app = Flask(__name__)

def v1_route(pattern):
    v1Route = '/todo/api/v1.0'
    return v1Route + pattern

def make_public_tasks(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

def makeTask(id, title, desc, done):
    return { 'id': id,
             'title': title,
             'description': desc,
             'done': done
           }

def find_task(task_id):
    return [task for task in tasks if task['id'] == task_id]

tasks = [
    makeTask(1, u'Buy groceries', u'Milk, Cheese, Fruit, Tylenol', False),
    makeTask(2, u'Learn python', u'Need to find one', False)
]

##########################CONTROLLER##########################################

@app.route(v1_route('/tasks'))
def get_tasks():
    return jsonify({'tasks': [make_public_tasks(task) for task in tasks]})

@app.route(v1_route('/tasks/<int:task_id>'), methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})

@app.route(v1_route('/tasks'), methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
            }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route(v1_route('/tasks/<int:task_id>'), methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if len(task) == 0:
        abort(404)

    tasks.remove(task[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)

