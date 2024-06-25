from flask import (Blueprint, g, request, redirect, render_template, url_for, flash)

from myapp.auth import login_required
from myapp.db import get_db

bp = Blueprint('qbank', __name__, url_prefix='/qbank')

import logging 

@bp.route('/questions', methods=['GET', 'POST'])
@login_required
def question():
    db = get_db()
    chapters = db.execute('SELECT id,title FROM Chapters').fetchall() # get to pass to form view
    question = db.execute('SELECT * FROM Questions LIMIT 1').fetchone()
    
    if request.method == 'POST':
        chapter_id = request.form.get('chapter-select')
        user_id = g.user['id']
        # get current state for that user
        current_state = db.execute('''SELECT * FROM currentState
                                  WHERE currentState.user_id = ?
                                 AND currentState.chapter_id = ? ''', (user_id, chapter_id)).fetchone()
        
        if current_state:# get question from Questions table
            question = db.execute(''' SELECT * FROM Questions 
                                  WHERE id = ? AND chapter_id = ?''', 
                                  (current_state['question_id'], chapter_id)).fetchone()
        if not current_state or not question:
            # First-time user or no current state, get the first question of the chapter
            question = db.execute('''
                SELECT * FROM Questions 
                WHERE chapter_id = ? 
                ORDER BY id ASC 
                LIMIT 1
            ''', (chapter_id,)).fetchone()
        if question:
            return render_template('qbank/questions_partial.html', question=question)
        else:
            return 'Please select a chapter to start.'
    # GET request
    return render_template('qbank/questions.html', chapters=chapters)


@bp.route('/answer', methods=['POST'])
@login_required
def answer():
    question_id = request.form['question_id']
    selected_answer = request.form['answer']
    
    db = get_db()
    question = db.execute('SELECT * FROM Questions WHERE Questions.id = ?', (question_id, )).fetchone()
    explaination = question['explaination']
    
    is_correct = question['correct_option'] == selected_answer

    # record user progress 
    db.execute('''INSERT OR REPLACE INTO Progress (user_id, question_id, answer, is_correct)
               VALUES (?,?,?,?)''', (g.user['id'], question_id, selected_answer, is_correct))
    db.commit()

    logging.debug(f"Debug: question_id : {question_id}, selected answer: {selected_answer}, corrrect: {question['correct_option']}, explaination: {explaination}")

    return render_template('qbank/answer_partial.html', is_correct = is_correct, explaination = explaination)
