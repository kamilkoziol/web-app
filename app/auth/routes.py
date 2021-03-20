from app import db
from app.models import User

from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.email import send_password_reset_email

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user

from werkzeug.urls import url_parse


@bp.route("/login", methods=['GET', 'POST'], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout", endpoint="logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("New user has been created")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Registration", form=form)


@bp.route('/reset_password_request', endpoint="reset_password_request", methods=["POST", "GET"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Follow instruction in mail to reset password")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request.html", title="reset", form=form)


@bp.route("/reset_password/<token>", endpoint="reset_password", methods=["POST", "GET"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Password has been changed")
        return redirect(url_for("main.index"))
    return render_template("auth/reset_password.html", form=form)
