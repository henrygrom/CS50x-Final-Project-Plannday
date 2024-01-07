from cs50 import SQL
from flask import Blueprint, render_template, request, session, redirect, url_for
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from forms import RegistrationForm, LoginForm

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///plannday.db")


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        form.process_data()
        username = form.username.data

        # Give session to user
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user in"""

    form = RegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        form.process_data()

        # Access form data
        firstname = form.first_name.data
        lastname = form.last_name.data
        username = form.username.data
        password = form.password.data

        # Insert user to database
        db.execute(
            "INSERT INTO users (username, hash, first_name, last_name) VALUES (?, ?, ?, ?);",
            username,
            generate_password_hash(password),
            firstname,
            lastname,
        )

        # Give session to user
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    else:
        return render_template("auth/register.html", form=form)
