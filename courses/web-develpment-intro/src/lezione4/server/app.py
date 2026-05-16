from flask import Flask, request, jsonify, Response, send_from_directory
import json
import os

app = Flask(__name__, static_folder="..")
FILE_PATH = 'tasks.json'

if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w') as f:
        json.dump([], f)

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    return Response('Accesso richiesto', 401, {'WWW-Authenticate': 'Basic realm="Login"'})

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with open(FILE_PATH, 'r') as f:
        return jsonify(json.load(f))

@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = json.load(open(FILE_PATH, 'r'))
    tasks.append(request.get_json())
    return jsonify({"status": "created"}), 201

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    tasks = json.load(open(FILE_PATH, 'r'))
    if 0 <= id < len(tasks):
        tasks.pop(id)
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Not found"}), 404

@app.route('/')
def index():
    return send_from_directory('..', 'index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
