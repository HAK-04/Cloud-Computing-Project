from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Configure database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_conn():
    """Establishes a PostgreSQL connection using the DATABASE_URL."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    url = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        host=url.hostname,
        port=url.port,
        database=url.path[1:],
        user=url.username,
        password=url.password
    )
    return conn

# Initialize database
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            deadline TEXT,
            team TEXT,
            person TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']
    team = request.form['team']
    person = request.form['person']
    status = request.form['status']

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, description, deadline, team, person, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (title, description, deadline, team, person, status))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('view_tasks'))

@app.route('/tasks')
def view_tasks():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/update_status', methods=['POST'])
def update_status():
    task_id = request.form['task_id']
    new_status = request.form['status']

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status, task_id))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)
