import sqlite3

def get_db():
    conn = sqlite3.connect('users.db')
    return conn

def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password_hash TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_account(username, password):   
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return True

def get_password(username):
   
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    