import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from auth import auth_bp, login_required

from forms import TaskForm

# Configure application
app = Flask(__name__)

app.register_blueprint(auth_bp)

# CSRF token for forms
app.config["SECRET_KEY"] = "this is a secret key for my cs50 project"

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///plannday.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]

    # Initialize task creation form
    form = TaskForm()

    if request.method == "POST" and form.validate_on_submit():
        # Initialize form data
        task_title = form.task_title.data
        task_description = form.task_description.data
        task_schedule = form.task_schedule.data

        # Insert task infos to task database
        db.execute(
            "INSERT INTO tasks (user_id, title, description, schedule, status) VALUES (?, ?, ?, ?, ?);",
            user_id,
            task_title,
            task_description,
            task_schedule,
            0,
        )

        return redirect("/")

    # Get task list of user
    morning_task = db.execute(
        "SELECT id, title, description FROM tasks WHERE user_id = ? AND schedule = 'morning' AND status = '0';",
        user_id,
    )
    afternoon_task = db.execute(
        "SELECT id, title, description FROM tasks WHERE user_id = ? AND schedule = 'afternoon' AND status = '0';",
        user_id,
    )
    evening_task = db.execute(
        "SELECT id, title, description FROM tasks WHERE user_id = ? AND schedule = 'evening' AND status = '0';",
        user_id,
    )

    return render_template(
        "main/index.html",
        form=form,
        morning_task=morning_task,
        afternoon_task=afternoon_task,
        evening_task=evening_task,
    )


@app.route("/update_task_status", methods=["POST"])
@login_required
def update_task_status():
    try:
        data = request.get_json()
        task_id = data["taskId"]
        is_checked = data["isChecked"]

        # Update the task status in the database
        db.execute("UPDATE tasks SET status = ? WHERE id = ?", is_checked, task_id)

        # Return a JSON response
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error updating task status: {str(e)}")
        return jsonify({"status": "error"})


@app.route("/completed_tasks", methods=["GET", "POST"])
@login_required
def completed_tasks():
    user_id = session["user_id"]

    # Get task list of user with status 1
    morning_task = db.execute(
        "SELECT id, title, description, status FROM tasks WHERE user_id = ? AND schedule = 'morning' AND status = '1';",
        user_id,
    )
    afternoon_task = db.execute(
        "SELECT id, title, description, status FROM tasks WHERE user_id = ? AND schedule = 'afternoon' AND status = '1';",
        user_id,
    )
    evening_task = db.execute(
        "SELECT id, title, description, status FROM tasks WHERE user_id = ? AND schedule = 'evening' AND status = '1';",
        user_id,
    )

    return render_template(
        "main/completedtask.html",
        morning_task=morning_task,
        afternoon_task=afternoon_task,
        evening_task=evening_task,
    )


@app.route("/delete_tasks", methods=["POST"])
@login_required
def delete_tasks():
    try:
        data = request.get_json()
        schedule = data["schedule"]

        # Delete the tasks from the database for the specified schedule
        db.execute(
            "DELETE FROM tasks WHERE user_id = ? AND schedule = ? AND status = 1;",
            session["user_id"],
            schedule,
        )

        # Return a JSON response
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error deleting tasks: {str(e)}")
        return jsonify({"status": "error"})


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

