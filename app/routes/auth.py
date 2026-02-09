from flask import Blueprint, request, render_template_string, redirect, url_for, session
from app.utils.db import get_db_connection
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # VULNERABILITY: 8. Weak password hashing (MD5 validation)
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # VULNERABILITY: 1. SQL Injection
        # Directly formatting the query with user input
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
        
        conn = get_db_connection()
        c = conn.cursor()
        try:
            # Executing raw SQL query directly
            c.execute(query)
            # Fetchone can be manipulated by SQL injection if multiple rows are expected, but here username is unique.
            # However, ' OR '1'='1 allows bypass.
            user = c.fetchone()
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('main.dashboard'))
            else:
                error = "Invalid credentials"
        except Exception as e:
            error = str(e)
        finally:
            conn.close()
            
    return f"""
    <h1>Login</h1>
    <p>Try SQL Injection: admin' OR '1'='1</p>
    {f'<p style="color:red">{error}</p>' if error else ''}
    <form method="POST">
        <label>Username: <input type="text" name="username"></label><br>
        <label>Password: <input type="password" name="password"></label><br>
        <input type="submit" value="Login">
    </form>
    <a href="{url_for('main.index')}">Home</a>
    """

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        conn = get_db_connection()
        c = conn.cursor()
        # VULNERABILITY: Still potentially vulnerable if input not sanitized, though parameterized here for functionality
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except Exception as e:
             return f"Error: {e}"
        finally:
            conn.close()
        return redirect(url_for('auth.login'))
        
    return """
    <h1>Register</h1>
    <form method="POST">
        <label>Username: <input type="text" name="username"></label><br>
        <label>Password: <input type="password" name="password"></label><br>
        <input type="submit" value="Register">
    </form>
    <a href="/">Home</a>
    """

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
