from flask import Flask, jsonify, abort, make_response, request, url_for
from response_function import response_200

app = Flask(__name__)

servers = [
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

def make_publish_server(server):
    new_server = {}
    for field in server:
        if field == 'id':
            new_server['uri'] = url_for('get_server', server_id=server['id'], _external=True)
        else:
            new_server[field] = server[field]
    return new_server

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/servers', methods=['GET'])
def get_servers():
    return jsonify({'servers': [make_publish_server(server) for server in servers]})

@app.route('/todo/api/v1.0/servers/<int:server_id>', methods=['GET'])
def get_server(server_id):
    server = [server for server in servers if server['id'] == server_id]
    if len(server) == 0:
        abort(400, description="write something for decorate error")
    return jsonify({'server': server[0]})

@app.route('/todo/api/v1.0/servers', methods=['POST'])
def create_server():
    if not request.json or not 'title' in request.json:
        abort(400, description="write something for decorate error")
    server = {
        'id': servers[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False,
    }
    servers.append(server)
    return jsonify({'server': server}), 201

@app.route('/todo/api/v1.0/servers/<int:server_id>', methods=['PUT'])
def update_server(server_id):
    server = [server for server in servers if server['id'] == server_id]
    print("aaaaaaaaaaaa")
    print(request.json)
    
    if len(server) == 0:
        abort(400, description="write something for decorate error")
    if not request.json:
        abort(400, description="write something for decorate error")
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400, description="write something for decorate error")
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400, description="write something for decorate error")
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400, description="write something for decorate error")
        
    server[0]['title'] = request.json.get('title', server[0]['title'])
    server[0]['description'] = request.json.get('title', server[0]['description'])
    server[0]['done'] = request.json.get('title', server[0]['done'])
    return jsonify({'server': server[0]})

@app.route('/todo/api/v1.0/servers/<int:server_id>', methods=['delete'])
def delete_server(server_id):
    server = [server for server in servers if server['id'] == server_id]
    if len(server) == 0:
        abort(400, description="write something for decorate error")
    servers.remove(server[0])
    return response_200({'result': True})

if __name__ == '__main__':
    app.run(debug=True)