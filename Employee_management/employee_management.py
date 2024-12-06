from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'employee_management.db'

# Initialize SQLite database
def init_db():
    """Create tables for employees, departments, and roles."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create Departments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        # Create Roles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        # Create Employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department_id INTEGER,
                role_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments(id),
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
        ''')
        conn.commit()

# Route: Home
@app.route('/')
def home():
    return render_template('index.html')

# Route: View Employees
@app.route('/employees')
def view_employees():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT employees.id, employees.name, departments.name, roles.name
            FROM employees
            LEFT JOIN departments ON employees.department_id = departments.id
            LEFT JOIN roles ON employees.role_id = roles.id
        ''')
        employees = cursor.fetchall()
    return render_template('employees.html', employees=employees)

# Route: Add Employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM departments')
        departments = cursor.fetchall()
        cursor.execute('SELECT * FROM roles')
        roles = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department_id']
        role_id = request.form['role_id']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO employees (name, department_id, role_id) VALUES (?, ?, ?)',
                           (name, department_id, role_id))
            conn.commit()
        return redirect(url_for('view_employees'))

    return render_template('add_employee.html', departments=departments, roles=roles)

# Route: Delete Employee
@app.route('/delete_employee/<int:id>')
def delete_employee(id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM employees WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('view_employees'))

# Route: Department-wise Employee Report
@app.route('/department_report')
def department_report():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT departments.name, COUNT(employees.id) AS employee_count
            FROM departments
            LEFT JOIN employees ON departments.id = employees.department_id
            GROUP BY departments.id
        ''')
        reports = cursor.fetchall()
    return render_template('department_report.html', reports=reports)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
