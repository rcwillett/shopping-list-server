from flask import (
    Blueprint,
    request,
    session
)
from flaskr.db import get_db
from .auth import login_required

bp = Blueprint('list', __name__, url_prefix='/list')

@bp.route('/getitems', methods=['GET'])
@login_required
def get_items():
    userid = session['user_id']
    if not userid:
        return 'User ID is required.', 400
    db = get_db()
    items = db.execute('SELECT id, name, quantity, purchased FROM item WHERE user_id = ?', (userid,)).fetchall()
    return {'items': items}, 200

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
    return 'Item updated successfully.', 200