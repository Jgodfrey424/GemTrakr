# -*- encoding: utf-8 -*-
import os
import logging
from flask import redirect, url_for, flash
from flask_login import current_user, login_user
from apps.authentication.models import User
from apps.firebase_init import db  # Ensure this is properly initialized

# 🚀 Removed GitHub OAuth since it's not needed

def login_user_firestore(username):
    """
    Authenticate user via Firestore and log them in.
    """
    try:
        users_ref = db.collection("users").where("username", "==", username).get()
        
        if users_ref:
            user_data = users_ref[0].to_dict()
            user = User(**user_data)  # Convert Firestore data into User object
            login_user(user)
            logging.info(f"✅ User {username} logged in successfully")
            return redirect(url_for('home_blueprint.index'))
        else:
            flash("User not found", "danger")
            return redirect(url_for('authentication_blueprint.login'))
    
    except Exception as e:
        logging.error(f"🔥 Firestore authentication error: {e}")
        flash("An error occurred during login.", "danger")
        return redirect(url_for('authentication_blueprint.login'))
