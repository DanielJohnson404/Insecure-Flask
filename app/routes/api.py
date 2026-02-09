from flask import Blueprint, request, jsonify, session
from app.utils.db import get_db_connection

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/message/<int:message_id>', methods=['GET'])
def get_message_unsafe(message_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM messages WHERE id = {message_id}")
    msg = c.fetchone()
    conn.close()
    
    if msg:
        return jsonify({'id': msg['id'], 'content': msg['content']})
    else:
        return jsonify({'error': 'Not found'}), 404

@api_bp.route('/message_safe/<int:message_id>', methods=['GET'])
def get_message_safe(message_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
    msg = c.fetchone()
    if not msg:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    current_user_id = session.get('user_id')
    if msg['sender_id'] != current_user_id and msg['receiver_id'] != current_user_id:
        conn.close()
        return jsonify({'error': 'Access Denied'}), 403
    conn.close()
    return jsonify({'id': msg['id'], 'content': msg['content']})
