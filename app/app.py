from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import socket
import os

app = Flask(__name__)

# Database connection settings (environment variables থেকে নেওয়া)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "taskdb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM tasks ORDER BY id")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks


def add_task(content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (content) VALUES (%s)", (content,))
    conn.commit()
    cursor.close()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/')
def home():
    hostname = socket.gethostname()
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks, hostname=hostname)


@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        add_task(task)
    return redirect(url_for('home'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('home'))


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)