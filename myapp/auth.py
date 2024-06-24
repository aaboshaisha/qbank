import functools

from flask import (Blueprint, request, render_template, redirect, url_for, flash, session, g )
from werkzeug.security import generate_password_hash, check_password_hash
from myapp.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        db = get_db()
        error = None

        if not valid_email(email):
            error = 'Please enter valid email address'
        elif not valid_password(password):
            error = 'Please enter valid password'
        elif not password == password2:
            error = 'Passwords must match'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Users (email, password) VALUES(?, ?)",
                    (email, generate_password_hash(password)), 
                    )
                db.commit()
            except db.IntegrityError: # will occur if the username already exists
                error = f"{email} is already registered."
            else:
                return redirect(url_for('auth.login'))
        
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        db = get_db()
        if not valid_email(email):
            error = 'Please enter valid email.'
        elif not valid_password(password):
            error = 'Please enter valid password.'   
        else:
            user = db.execute('SELECT * FROM Users WHERE email = ?',list (email,)).fetchone()
            if user is None:
                error = 'Incorrect email.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password'
            else:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id') # the one we stored above in login

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM Users WHERE id = ?', (user_id, )).fetchone()
        

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# input validation functions
import re

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
PASS_RE = re.compile(r'^.{3,20}$')

def valid_email(email):
    return EMAIL_RE.match(email)

def valid_password(password):
    return PASS_RE.match(password)

