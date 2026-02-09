from flask import Blueprint
from app.utils.config import Config
from app.utils.db import get_db_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_panel():
    # VULNERABILITY: 7. Missing authentication on admin endpoints
    users = []
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        for row in rows:
            users.append({'id': row['id'], 'username': row['username'], 'password': row['password']})
        conn.close()
    except:
        pass

    users_html = "".join([f"<li>{u['username']} (Pass Hash: {u['password']})</li>" for u in users])
    return f"""
    <h1>Admin Panel - TOP SECRET</h1>
    <p>Manage Users:</p>
    <ul>{users_html}</ul>
    <p>System Env:<br> AWS_SECRET: {Config.AWS_SECRET_ACCESS_KEY}</p>
    <a href="/">Home</a>
    """
