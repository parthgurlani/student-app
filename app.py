from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="testdb"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    marks = request.form['marks']

    db = get_db()
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), marks INT)")
    cursor.execute("INSERT INTO students (name, marks) VALUES (%s, %s)", (name, marks))

    db.commit()
    return redirect('/view')

@app.route('/view')
def view():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    return render_template('view.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)