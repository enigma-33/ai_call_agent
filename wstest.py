from flask import Flask, jsonify, request

import uuid

app = Flask(__name__)

tasks = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruits',
        'completed': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Learn Python',
        'description': 'Learn how to create a web service with Python',
        'completed': True
    }
]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = {
        'id': uuid.uuid4().hex,
        'title': request.json['title'],
        'description': request.json['description'],
        'completed': request.json.get('completed', False)
    }
    tasks.append(new_task)
    return jsonify({'task': new_task})

@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': 'Task not found'})
    return jsonify({'task': task[0]})

@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': 'Task not found'})
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['completed'] = request.json.get('completed', task[0]['completed'])
    return jsonify({'task': task[0]})

@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': 'Task not found'})
    tasks.remove(task[0])
    return jsonify({'result': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)