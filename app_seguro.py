from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    INSERT INTO users (username, password)
    SELECT 'johndoe', '12345'
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'johndoe')
    """)
    cursor.execute("""
    INSERT INTO users (username, password)
    SELECT 'maryjane', 'password123'
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'maryjane')
    """)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            return f"Login successful! Welcome, {user['username']}."
        else:
            return "Login failed! Invalid credentials."

    return render_template('login.html')

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
