import os
import random
import json
from flask import render_template, redirect, url_for, request, jsonify

from educhat import app
from educhat.models import Exercise, TeachingAssistant

ta = TeachingAssistant()
exercise = None
topic = None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_topic', methods=['POST'])
def select_topic():
    global topic
    _topic = request.form['topic']
    if _topic:  
        topic = _topic
        return jsonify(success=True)
    else:
        return jsonify({'error': 'No topic selected'}), 400

@app.route('/random_exercise', methods=['GET'])
def random_exercise():
    global exercise
    global ta
    global topic
    topic_dir = os.path.join('res', topic)
    task_dirs = [d for d in os.listdir(topic_dir) if os.path.isdir(os.path.join(topic_dir, d))]

    if exercise is not None and len(task_dirs) > 1:
        task_dirs.remove(exercise.name)

    selected_task = random.choice(task_dirs)

    exercise = Exercise(topic, selected_task)
    ta.reset()
    return redirect(url_for('exercise_page'))

@app.route('/exercise', methods=['GET'])
def exercise_page():
    global exercise
    if exercise is not None:
        return render_template('exercise.html', task_description=exercise.describe())
    else:
        return redirect(url_for('index'))
    
@app.route('/chat', methods=['POST'])
def chat():
    global exercise
    global ta
    student_answer = request.form['student_answer']
    if exercise is not None and student_answer is not None:
        ta_answer = ta.chat(exercise, student_answer)
        return jsonify({'ta_answer': ta_answer})
    else:
        return jsonify({'error': 'No exercise selected'}), 400
    
@app.route('/hint', methods=['POST'])
def hint():
    global exercise
    global ta
    if exercise is not None:
        ta_answer = ta.hint(exercise)
        return jsonify({'hint': ta_answer})
    else:
        return jsonify({'error': 'No exercise selected'}), 400
    

@app.route('/new-task')
def new_task():
    return render_template('new_task.html')

@app.route('/check-task-name', methods=['POST'])
def check_task_name():
    global topic
    taskName = request.json['taskName']
    taskPath = os.path.join('res', topic, taskName)
    return jsonify(unique=not os.path.exists(taskPath))

@app.route('/save-task', methods=['POST'])
def save_task():
    global topic
    taskName = request.form['task-name']
    taskDescription = request.form['task-description']
    taskSolution = request.form['task-solution']
    markingScheme = request.form['marking-scheme']
    
    taskPath = os.path.join('res', topic, taskName)
    os.makedirs(taskPath, exist_ok=False)
    
    try:
        with open(os.path.join(taskPath, 'task.txt'), 'w') as file:
            file.write(taskDescription)
        with open(os.path.join(taskPath, 'solution.txt'), 'w') as file:
            file.write(taskSolution)
        with open(os.path.join(taskPath, 'marking.txt'), 'w') as file:
            file.write(markingScheme)
        return jsonify(success=True)
    except:
        return jsonify(success=False)

@app.route('/task-saved')
def task_saved():
    return 'Thank you, we saved the exercise. <a href="/new-task">Add Another</a> | <a href="/random_exercise">Start Solving</a>'

@app.route('/topics')
def topics():
    topic_dirs = [d for d in os.listdir('res') if os.path.isdir(os.path.join('res', d))]
    topics = []
    for d in topic_dirs:
        with open(f'res/{d}/metadata.json') as f:
            metadata = json.load(f)
        topics.append({
            'folder': d,
            'name': metadata['name'],
            'icon': metadata['icon']
        })
    return jsonify({'topics': topics})