"""TODO"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


from project.models import User

from . import db

auth = Blueprint(
    "auth", __name__, template_folder="../templates", static_folder="../static"
)


@auth.route("/login")
def login():
    """Login page (GET)"""
    return render_template("login.html")


@auth.route("/signup")
def signup():
    """SignUp page (GET)"""
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    """SignUp Page POST"""
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    """LogOut Page"""
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/login", methods=["POST"])
def login_post():
    """LogIn Page POST"""
    email = request.form.get("email")
    password = request.form.get("password")
    remember = bool(request.form.get("remember"))

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    return redirect(url_for("main.games"))
