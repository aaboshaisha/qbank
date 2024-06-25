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
    question = db.execute('SELECT * FROM Questions LIMIT 1')

    if request.method == 'POST':
        chapter_id = request.form.get('chapter-select')
        user_id = g.user['id']
        # get current state for that user
        question_id = db.execute('''SELECT question_id FROM currentState
                                  WHERE currentState.user_id = ?
                                 AND currentState.chapter_id = ? ''', (user_id, chapter_id)).fetchone()
        
        # get question from Questions table
        question = db.execute(''' SELECT * FROM Questions 
                              WHERE id = ? AND chapter_id = ?''', (question_id, chapter_id)).fetchone()
        if question is None:
            question = db.execute('SELECT * FROM Questions WHERE chapter_id = ?', (chapter_id, )).fetchone()
        return render_template('qbank/questions_partial.html', question=question)
    
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

