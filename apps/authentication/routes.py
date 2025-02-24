# -*- encoding: utf-8 -*-
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from flask_dance.contrib.github import github

from apps import login_manager
from apps.authentication import blueprint
from google.cloud import firestore
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import User

from apps.authentication.util import verify_pass

db = firestore.Client()

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))
    
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        users_ref = db.collection("users").where("username", "==", username).get()

        if users_ref:
            user_data = users_ref[0].to_dict()
            user = User(**user_data)  # Convert Firestore document into a User object
        else:
            user = None


        # Check the password
        if user and User.check_password(password, user.password_hash):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username already exists in Firestore
        users_ref = db.collection("users").where("username", "==", username).get()
        if users_ref:
            return render_template('accounts/register.html',
                                   msg='Username already taken',
                                   success=False,
                                   form=create_account_form)

        # Check if email already exists
        email_ref = db.collection("users").where("email", "==", email).get()
        if email_ref:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # Create new user dictionary
        user_data = {
            "id": email,  # Using email as a unique identifier
            "username": username,
            "email": email,
            "password_hash": User.hash_password(password),
            "oauth_github": None
        }

        # Save user to Firestore
        db.collection("users").document(username).set(user_data)

        logout_user()  # Ensure user is logged out before registration confirmation

        return render_template('accounts/register.html',
                               msg='Account created successfully. You can now log in.',
                               success=True,
                               form=create_account_form)

    return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
