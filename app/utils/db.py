import sqlite3
from app.utils.config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, content TEXT)''')
    
    # Check if admin exists
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES ('admin', '5f4dcc3b5aa765d61d8327deb882cf99')") # md5(password)
    
    # Create some dummy messages for IDOR
    c.execute("SELECT * FROM messages")
    if not c.fetchone():
        c.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (1, 2, 'Secret admin message')")
        c.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (2, 1, 'Hello admin')")
        
    conn.commit()
    conn.close()
