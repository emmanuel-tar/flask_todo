from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(10), nullable=False, default="Low")


# Create database
with app.app_context():
    db.create_all()


# Home page
@app.route("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks)


# Add task
@app.route("/add", methods=["POST"])
def add_task():
    content = request.form["content"]
    priority = request.form["priority"]
    new_task = Task(content=content, priority=priority)

    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


# Delete task
@app.route("/delete/<int:id>")
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("index"))


# Update task
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_task(id):
    task = Task.query.get(id)
    if request.method == "POST":
        task.content = request.form["content"]
        task.priority = request.form["priority"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
