from cs50 import SQL
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    BooleanField,
    validators,
)
from wtforms.validators import ValidationError
from werkzeug.security import check_password_hash

db = SQL("sqlite:///plannday.db")


class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First Name",
        [
            validators.DataRequired(),
            validators.Regexp(
                "^[A-Za-z ]*$", message="First Name should contain letters only"
            ),
        ],
    )

    last_name = StringField(
        "Last Name",
        [
            validators.DataRequired(),
            validators.Regexp(
                "^[A-Za-z ]*$", message="Last Name should contain letters only"
            ),
        ],
    )

    username = StringField(
        "Username",
        [
            validators.DataRequired(),
            validators.Length(min=4, max=25),
            validators.Regexp("^[a-zA-Z0-9_]+$", message="Invalid Username"),
        ],
    )

    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.Length(min=6, message="Password must be 6 characters long."),
            validators.Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]*$",
                message="Password must contain at least 1 uppercase, 1 lowercase, 1 special character, and 1 number",
            ),
        ],
    )

    password_confirmation = PasswordField(
        "Repeat Password",
        [
            validators.EqualTo("password", message="Password must match"),
        ],
    )

    # Converts data to avoid duplication error
    def process_data(self):
        self.first_name.data = self.first_name.data.title()
        self.last_name.data = self.last_name.data.title()
        self.username.data = self.username.data.lower()

    # Check for username duplication
    def validate_username(form, field):
        # Make the username case insensitive
        field.data = field.data.lower()

        # Query database for username
        username_exist = db.execute(
            "SELECT * FROM users WHERE username = ?", field.data
        )

        if len(username_exist) > 0:
            raise ValidationError("Username already taken")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        [
            validators.DataRequired(),
            validators.Length(min=4, max=25),
            validators.Regexp("^[a-zA-Z0-9_]+$", message="Invalid Username"),
        ],
    )

    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
        ],
    )

    # Convert data to lower to avoid ducplication error
    def process_data(self):
        self.username.data = self.username.data.lower()

    # Check if username exists
    def validate_username(form, field):
        # Make the username case insensitive
        field.data = field.data.lower()

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", field.data)

        if len(rows) != 1:
            raise ValidationError("Username does not exist")

    # Check if password match the username
    def validate_password(form, field):
        # Query database for username
        username = db.execute(
            "SELECT * FROM users WHERE username = ?", form.username.data
        )

        if len(username) == 1:
            if not check_password_hash(username[0]["hash"], field.data):
                raise ValidationError("Invalid password")


class TaskForm(FlaskForm):
    def validate_task_schedule(form, field):
        valid = [choice[0] for choice in field.choices]

        if field.data not in valid:
            raise ValidationError("Invalid option")

    task_title = StringField(
        "Title",
        [
            validators.DataRequired(),
            validators.Length(max=50),
        ],
    )

    task_description = TextAreaField(
        "Description",
        [
            validators.Length(max=500),
        ],
    )

    task_schedule = SelectField(
        "Schedule",
        [validators.DataRequired(), validate_task_schedule],
        choices=[
            ("morning", "Morning"),
            ("afternoon", "Afternoon"),
            ("evening", "Evening"),
        ],
    )
