import functools
from flask import (
    Blueprint, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if not username:
            return 'Username is required.', 400
        if not password:
            return 'Password is required.', 400
        db = get_db()
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()

        except db.IntegrityError:
            return f"User {username} is already registered.", 400
        else: 
            return "User registered successfully", 200
        
@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if not username:
            return 'Username is required.', 400
        if not password:
            return 'Password is required.', 400
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT id, username, password FROM user WHERE username = ?', (username,))
        user = cur.fetchone()
        if not user:
            raise Exception(f"User {username} does not exist.")
        if not check_password_hash(user['password'], password):
            raise Exception("Password is incorrect.")
        session['user_id'] = user['id']
        session.modified = True
        return 'Login successful.', 200
    
@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return 'Logout successful.', 200

def login_required(route):
    @functools.wraps(route)
    def wrapped_route(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return 'Unauthorized', 401
        return route(*args, **kwargs)
    return wrapped_route