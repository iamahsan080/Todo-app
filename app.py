from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# simple in-memory store
todos = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Build CI/CD", "done": False}
]

@app.route('/')
def home():
    return "Welcome to Flask Todo API!"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json() or {}
    if 'task' not in data:
        return jsonify({"error": "task is required"}), 400
    new_todo = {"id": len(todos) + 1, "task": data['task'], "done": False}
    todos.append(new_todo)
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "not found"}), 404
    data = request.get_json() or {}
    todo["task"] = data.get("task", todo["task"])
    todo["done"] = data.get("done", todo["done"])
    return jsonify(todo), 200

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"message": "deleted"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    if os.getenv("CANARY", "false").lower() == "true":
        print("🟡 CANARY MODE ENABLED")
    app.run(host='0.0.0.0', port=port)
