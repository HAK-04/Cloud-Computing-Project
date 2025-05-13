from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
tasks = []  # In-memory list to store tasks

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
    task_id = len(tasks) + 1
    tasks.append({
        'id': task_id,
        'title': title,
        'description': description,
        'deadline': deadline,
        'team': team,
        'person': person,
        'status': status
    })
    return redirect(url_for('view_tasks'))

@app.route('/tasks')
def view_tasks():
    return render_template('tasks.html', tasks=tasks)

@app.route('/update_status', methods=['POST'])
def update_status():
    task_id = int(request.form['task_id'])
    new_status = request.form['status']
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            break
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)
