from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
DATABASE = 'user_data.db'

def init_db():
    """Create a SQLite database with a table for storing user details."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL
            )
        ''')
        conn.commit()

# Route to display the form
@app.route('/')
def index():
    return '''
    <h3>Enter Your Details</h3>
    <form method="post" action="/submit">
        Name: <input type="text" name="name" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        Age: <input type="number" name="age" min="1" required><br><br>
        <input type="submit" value="Submit">
    </form>
    '''

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    # Insert user data into the database
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', (name, email, age))
            conn.commit()
        return '<h3>Details submitted successfully!</h3><a href="/">Go Back</a>'
    except sqlite3.IntegrityError:
        return '<h3>Email already exists! Please use a different email.</h3><a href="/">Go Back</a>'

# Route to display all user details
@app.route('/users')
def users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
    user_list = "<h3>Registered Users:</h3><ul>"
    for user in rows:
        user_list += f"<li>ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Age: {user[3]}</li>"
    user_list += "</ul><a href='/'>Go Back</a>"
    return user_list

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5555, debug=True)
