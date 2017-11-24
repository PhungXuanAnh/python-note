from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from curses.has_key import python

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'descriptioni': 'Milk, Cheese, Pizza, Fruit',
        'done': False,
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'You need to find a good python tutorial in the web',
        'done': False,
    },
]
def make_publish_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
#     return jsonify({'tasks': tasks})
    return jsonify({'tasks': [make_publish_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False,
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
        
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('title', task[0]['description'])
    task[0]['done'] = request.json.get('title', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['delete'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

#========================================================
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'xuananh':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 404)

if __name__ == '__main__':
    app.run(debug=True)