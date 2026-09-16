from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DATABASE = "instance/tasks.db"

Path("instance").mkdir(exist_ok=True)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def task_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"])
    }

@app.get("/tasks")
def get_tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    conn.close()
    return jsonify([task_to_dict(r) for r in rows]), 200

@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task_to_dict(row)), 200

@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    title = data.get("title")
    description = data.get("description", "")
    completed = data.get("completed", False)

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "title is required and must be a non-empty string"}), 400
    if not isinstance(description, str):
        return jsonify({"error": "description must be a string"}), 400
    if not isinstance(completed, bool):
        return jsonify({"error": "completed must be true or false"}), 400

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (title.strip(), description, int(completed))
    )
    conn.commit()
    task_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    return jsonify(task_to_dict(row)), 201

@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    title = data.get("title", row["title"])
    description = data.get("description", row["description"])
    completed = data.get("completed", bool(row["completed"]))

    if not isinstance(title, str) or not title.strip():
        conn.close()
        return jsonify({"error": "title must be a non-empty string"}), 400
    if not isinstance(description, str):
        conn.close()
        return jsonify({"error": "description must be a string"}), 400
    if not isinstance(completed, bool):
        conn.close()
        return jsonify({"error": "completed must be true or false"}), 400

    conn.execute(
        "UPDATE tasks SET title=?, description=?, completed=? WHERE id=?",
        (title.strip(), description, int(completed), task_id)
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()

    return jsonify(task_to_dict(updated)), 200

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted successfully"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
