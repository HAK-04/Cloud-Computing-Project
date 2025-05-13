from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    deadline TEXT,
                    team TEXT,
                    person TEXT,
                    status TEXT DEFAULT 'Pending'
                )''')
    conn.commit()
    conn.close()

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

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, deadline, team, person, status) VALUES (?, ?, ?, ?, ?, ?)",
              (title, description, deadline, team, person, status))
    conn.commit()
    conn.close()

    return redirect(url_for('view_tasks'))

@app.route('/tasks')
def view_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/update_status', methods=['POST'])
def update_status():
    task_id = request.form['task_id']
    new_status = request.form['status']

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)
