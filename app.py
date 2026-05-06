from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup (replaces load_from_file)
def init_db():
    with sqlite3.connect("todos.db") as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS todos (
                     id INTEGER PRIMARY KEY, 
                     task TEXT,
                     done INTEGER DEFAULT 0
                     )
                     """)
init_db()

# view tasks (replace view_tasks)
@app.route("/")
def home():
    with sqlite3.connect("todos.db") as conn:
        todos = conn.execute("SELECT * FROM todos").fetchall()
    return render_template("index.html", todos=todos)

# add task (replaces add_task)
@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"].strip()
    if task == "":
        return redirect("/")
    with sqlite3.connect("todos.db") as conn:
        conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    return redirect("/")

# complete task
@app.route("/complete/<int:id>")
def complete(id):
    with sqlite3.connect("todos.db") as conn:
        conn.execute("UPDATE todos SET done=1 WHERE id=?", (id,))
    return redirect("/")

#  delete taks (replaces delete_task)
@app.route("/delete/<int:id>")
def delete(id):
    with sqlite3.connect("todos.db") as conn:
        conn.execute("DELETE FROM todos WHERE id=?", (id,))
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
