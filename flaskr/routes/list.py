from flask import (
    Blueprint,
    request,
    session
)
import json
from flaskr.db import get_db
from .auth import login_required

bp = Blueprint('list', __name__, url_prefix='/list')

@bp.route('/getitems', methods=['GET'])
@login_required
def get_items():
    userid = int(session.get('user_id'))
    if not userid:
        return 'User ID is required.', 400
    db = get_db()
    cur = db.cursor()
    items = cur.execute('SELECT id, name, quantity, purchased FROM item WHERE user_id = ?', (userid,)).fetchall()
    db.commit()
    results = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in items]
    json_output = json.dumps(results)
    return json_output, 200

@bp.route('/create', methods=['POST'])
@login_required
def create_item():
    user_id = session['user_id']
    name = request.json['name']
    quantity = request.json['quantity']
    if not name:
        return 'Name is required.', 400
    if not quantity:
        return 'Quantity is required.', 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO item (user_id, name, quantity) VALUES (?, ?, ?)', (user_id, name, quantity))
    db.commit()
    return { 'item_id': cursor.lastrowid }, 200

@bp.route('/remove', methods=['POST'])
@login_required
def remove_item():
    item_id = request.json['item_id']
    if not item_id:
        return 'Item ID is required.', 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM item WHERE id = ?', (item_id,))
    db.commit()
    return 'Item removed successfully.', 200

@bp.route('/update', methods=['POST'])
@login_required
def update_item():
    item_id = request.json['item_id']
    name = request.json['name']
    quantity = request.json['quantity']
    if not item_id:
        return 'Item ID is required.', 400
    if not name:
        return 'Name is required.', 400
    if not quantity:
        return 'Quantity is required.', 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE item SET name = ?, quantity = ? WHERE id = ?', (name, quantity, item_id))
    db.commit()
    return 'Item updated successfully.', 200

@bp.route('/purchased', methods=['POST'])
@login_required
def purchased_item():
    item_id = request.json['item_id']
    if not item_id:
        return 'Item ID is required.', 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE item SET purchased = 1 WHERE id = ?', (item_id,))
    db.commit()
    return 'Item updated successfully.', 200