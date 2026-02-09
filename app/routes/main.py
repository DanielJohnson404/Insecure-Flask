from flask import Blueprint, request, render_template_string, redirect, url_for, session, send_file, make_response
from app.utils.db import get_db_connection
from app.utils.config import Config
import pickle
import base64

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # VULNERABILITY: 5. Insecure deserialization
    prefs = request.cookies.get('prefs')
    user_prefs = {}
    if prefs:
        try:
            user_prefs = pickle.loads(base64.b64decode(prefs))
        except:
            pass
            
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM comments")
    comments = c.fetchall()
    conn.close()
    
    comments_html = "<ul>"
    for comment in comments:
        # VULNERABILITY: 2. Cross-Site Scripting (XSS)
        comments_html += f"<li>{comment['content']}</li>"
    comments_html += "</ul>"
    
    return f"""
    <h1>Vulnerable Flask App (Modular)</h1>
    <p>Welcome! <a href="{url_for('auth.login')}">Login</a> | <a href="{url_for('auth.register')}">Register</a> | <a href="{url_for('main.dashboard')}">Dashboard</a> | <a href="{url_for('admin.admin_panel')}">Admin Panel</a></p>
    <h2>Comments</h2>
    {comments_html}
    <form action="{url_for('main.add_comment')}" method="POST">
        <input type="text" name="content" placeholder="Leave a comment">
        <input type="submit" value="Post">
    </form>
    <br>
    <a href="{url_for('files.list_files')}">View File Service</a>
    <br>
    <h2>Network Tools</h2>
    <form action="{url_for('network.ping_unsafe')}" method="POST">
        <input type="text" name="address" placeholder="IP Address (e.g. 8.8.8.8)">
        <input type="submit" value="Ping (Unsafe)">
    </form>
    <form action="{url_for('network.ping_safe')}" method="POST">
        <input type="text" name="address" placeholder="IP Address (e.g. 8.8.8.8)">
        <input type="submit" value="Ping (Safe)">
    </form>
    """

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # IDOR Example Link
    idor_links = ""
    # Assuming user 1 wants to see message 1
    # Assuming attacker wants to see message 2 (sent by user 2 to user 1)
    
    return f"""
    <h1>Dashboard</h1>
    <p>Welcome, {session.get('username', 'User')}!</p>
    <p>API Key: {Config.AWS_ACCESS_KEY_ID} (Leaked!)</p>
    <a href="{url_for('files.upload_file')}">Upload File</a> | <a href="{url_for('auth.logout')}">Logout</a>
    <hr>
    <h3>Messaging (IDOR Demo)</h3>
    <p>Try accessing these message endpoints:</p>
    <ul>
        <li><a href="{url_for('api_bp.get_message_unsafe', message_id=1)}">Message 1 (Unsafe)</a></li>
        <li><a href="{url_for('api_bp.get_message_safe', message_id=1)}">Message 1 (Safe)</a></li>
    </ul>
    """

@main_bp.route('/comment', methods=['POST'])
def add_comment():
    content = request.form.get('content')
    if content:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO comments (content) VALUES (?)", (content,))
        conn.commit()
        conn.close()
    return redirect(url_for('main.index'))
    
@main_bp.route('/set_cookie')
def set_cookie_demo():
    data = {'theme': 'dark', 'admin': False}
    pickled = base64.b64encode(pickle.dumps(data)).decode()
    resp = make_response("Cookie set! Check 'prefs' cookie.")
    resp.set_cookie('prefs', pickled)
    return resp
