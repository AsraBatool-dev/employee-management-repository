"""
Employee Management System
A Flask-based CRUD application for managing employee records.
Author: Asra Batool
Database: SQLite3
"""

from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    """Establish database connection with SQLite3"""
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and create table if not exists"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Employee Management System</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px; min-height: 100vh;
        }
       .container {
            max-width: 1100px; margin: auto; background: white;
            padding: 40px; border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #2c3e50; text-align: center; margin-bottom: 10px;
            font-size: 32px;
        }
       .subtitle {
            text-align: center; color: #7f8c8d; margin-bottom: 30px;
            font-size: 14px;
        }
        h2 {
            color: #34495e; border-bottom: 3px solid #3498db;
            padding-bottom: 10px; margin: 30px 0 20px 0;
        }
        form {
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 15px; margin-bottom: 30px;
            background: #f8f9fa; padding: 25px; border-radius: 10px;
        }
        input {
            padding: 14px; border: 2px solid #e0e0e0;
            border-radius: 8px; font-size: 14px;
            transition: all 0.3s;
        }
        input:focus {
            outline: none; border-color: #3498db;
        }
        button {
            grid-column: span 2; padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 8px;
            cursor: pointer; font-size: 16px; font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        table {
            width: 100%; border-collapse: collapse;
            margin-top: 20px; overflow: hidden;
            border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 15px; text-align: left;
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; font-weight: 600;
        }
        tr:nth-child(even) { background: #f8f9fa; }
        tr:hover { background: #e3f2fd; }
       .actions a {
            text-decoration: none; padding: 8px 16px;
            border-radius: 6px; font-weight: 500;
            transition: all 0.3s;
        }
       .delete {
            background: #e74c3c; color: white;
        }
       .delete:hover { background: #c0392b; }
       .footer {
            text-align: center; margin-top: 40px;
            color: #95a5a6; font-size: 13px;
            padding-top: 20px; border-top: 1px solid #ecf0f1;
        }
       .empty { text-align: center; padding: 40px; color: #95a5a6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Employee Management System</h1>
        <p class="subtitle">Full Stack CRUD Application | python flask + SQLite3</p>

        <h2>➕ Add New Employee</h2>
        <form method="POST" action="/add">
            <input name="name" placeholder="Full Name" required>
            <input name="email" placeholder="Email Address" type="email" required>
            <input name="department" placeholder="Department" required>
            <input name="salary" type="number" placeholder="Salary" required>
            <button type="submit">Add Employee to Database</button>
        </form>

        <h2>👥 All Employees</h2>
        {% if employees %}
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Salary</th>
                <th>Actions</th>
            </tr>
            {% for emp in employees %}
            <tr>
                <td><strong>#{{ emp[0] }}</strong></td>
                <td>{{ emp[1] }}</td>
                <td>{{ emp[2] }}</td>
                <td>{{ emp[3] }}</td>
                <td><strong>${{ emp[4] }}</strong></td>
                <td class="actions">
                    <a href="/delete/{{ emp[0] }}" class="delete" onclick="return confirm('Delete {{ emp[1] }}?')">🗑️ Delete</a>
                </td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <div class="empty">
            <h3>No employees yet!</h3>
            <p>Add your first employee using the form above </p>
        </div>
        {% endif %}

        <div class="footer">
            Employee Management System | python Flask + SQLite3
            
        </div>
    </div>
</body>
</html>
'''

# Routes - Yehi Tera Backend Logic Hai
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees ORDER BY id DESC")
    employees = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template_string(HTML, employees=employees)

@app.route('/add', methods=['POST'])
def add():
    db = get_db()
    cursor = db.cursor()
    sql = "INSERT INTO employees (name, email, department, salary) VALUES (?, ?, ?, ?)"
    val = (request.form['name'], request.form['email'], request.form['department'], request.form['salary'])
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect('/')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Employee Management System is running!")
    print("="*50)
    print("Open your browser and go to:")
    print("Server running at: http://localhost:5000 ")
    print("="*50 + "\n")
    app.run(debug=True)