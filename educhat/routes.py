import os
import random
from flask import session, render_template, redirect, url_for, request, jsonify

from educhat import app
from educhat.models import Exercise, TeachingAssistant

ta = TeachingAssistant()
exercise = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_exercise', methods=['GET'])
def random_exercise():
    global exercise
    task_dirs = [d for d in os.listdir('res') if os.path.isdir(os.path.join('res', d))]
    selected_task = random.choice(task_dirs)
    exercise = Exercise(f'res/{selected_task}')
    return redirect(url_for('exercise_page'))

@app.route('/exercise', methods=['GET'])
def exercise_page():
    global exercise
    if exercise is not None:
        return render_template('exercise.html', task_description=exercise.describe())
    else:
        return redirect(url_for('index'))
    
@app.route('/evaluate', methods=['POST'])
def evaluate():
    global exercise
    global ta
    print("Evaluating")
    student_answer = request.form['student_answer']
    print("Student answer: ", student_answer)
    if exercise is not None and student_answer is not None:
        evaluation = ta.mark(exercise, student_answer)
        print('Finished evaluation', evaluation)
        return jsonify({'evaluation': evaluation})
    else:
        print('Error: No exercise selected')
        return jsonify({'error': 'No exercise selected'}), 400