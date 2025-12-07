"""Authentication blueprint: signup, login, and logout.

This module defines the routes and helpers for user authentication.
It contains a `validate_form` helper used by signup to provide
beginner-friendly validation and clear flash messages.
"""

from flask import Blueprint, render_template, redirect, request, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

# Create a blueprint so these routes can be registered with the app.
auth = Blueprint("auth", __name__)


def validate_form(email, password, name=None, confirm_password=None):
    """Validate signup form fields.

    - `name` and `confirm_password` are optional when used for login,
      but required/checked for signup.
    - Uses `flash` to communicate friendly error messages to templates.
    """

    # ---- NAME (SIGNUP ONLY) ----
    if name is not None:
        # Make sure name is a non-empty string
        if not isinstance(name, str) or not name.strip():
            flash("Name is required.", "error")
            return False
        # Length checks for beginner-friendly UX
        if len(name) < 3:
            flash("Name must be at least 3 characters.", "error")
            return False
        if len(name) > 30:
            flash("Name must be under 30 characters.", "error")
            return False
        # Allow letters, numbers, underscores and hyphens only
        if not name.replace("_", "").replace("-", "").isalnum():
            flash(
                "Name may contain letters, numbers, underscores, or hyphens only.",
                "error",
            )
            return False

    # ---- EMAIL ----
    if not email:
        flash("Email is required.", "error")
        return False
    # Very simple email format check — for production use a proper validator
    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Invalid email format.", "error")
        return False

    # ---- PASSWORD ----
    if not password:
        flash("Password is required.", "error")
        return False
    if len(password) < 8:
        flash("Password must be at least 8 characters.", "error")
        return False
    # Require both letters and numbers for simple strength
    if password.isdigit() or password.isalpha():
        flash("Password must include letters and numbers.", "error")
        return False
    # Require mixed case for a small extra strength check
    if password.lower() == password or password.upper() == password:
        flash("Password must include uppercase and lowercase letters.", "error")
        return False

    # ---- CONFIRM PASSWORD (SIGNUP ONLY) ----
    if confirm_password is not None:
        if not confirm_password:
            flash("Confirm password is required.", "error")
            return False
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return False

    return True


# ---------------------------------------------------------------
# SIGNUP
# ---------------------------------------------------------------
@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    """Handle user signup (create account).

    - On GET: render signup form.
    - On POST: validate input, create user (hashed password), login user.
    """
    if request.method == "POST":
        # Get form values from the POST request
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")  # matches template

        # Validate input and show helpful messages on failure
        if not validate_form(email, password, name, confirm_password):
            return render_template("signup.html")

        # Prevent duplicate accounts using the same email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists. Try logging in instead.", "error")
            return render_template("signup.html")

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, name=name, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            # Rollback on error and show a friendly message
            db.session.rollback()
            flash("An error occurred creating your account.", "error")
            print("DB ERROR:", e)
            return render_template("signup.html")

        # Log the user in immediately after signup
        login_user(new_user, remember=True)
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("views.home", new_user=True))

    # Render signup page for GET requests. `user=current_user` allows the
    # template to render user information if already logged in.
    return render_template("signup.html", user=current_user)


# ---------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login.

    On POST, verify the email exists and the password matches the
    stored (hashed) password. On success, the user is logged in.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Basic validation — login only needs the fields present
        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html")

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User does not exist.", "error")
            return render_template("login.html")

        # Compare the hashed password
        if not check_password_hash(user.password, password):
            flash("Incorrect password.", "error")
            return render_template("login.html")

        # Login the user and redirect to home
        login_user(user, remember=True)
        flash("Logged in successfully!", "success")
        return redirect(url_for("views.home", new_user=False))

    return render_template("login.html", user=current_user)


# ---------------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------------
@auth.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to the login page."""
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))
