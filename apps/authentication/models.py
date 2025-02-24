# -*- encoding: utf-8 -*-
"""
Modified from AppSeed.us - Now using Firestore instead of SQLAlchemy
"""

from flask_login import UserMixin
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from werkzeug.security import generate_password_hash, check_password_hash
from apps import login_manager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase only once
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")

    if not cred_path or not os.path.exists(cred_path):
        raise ValueError("❌ FIREBASE_SERVICE_ACCOUNT_KEY is missing or incorrect.")

    cred = credentials.Certificate(cred_path)
    initialize_app(cred)

# Now that Firebase is initialized, create Firestore client
db = firestore.client()

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, oauth_github=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.oauth_github = oauth_github

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(password, password_hash):
        return check_password_hash(password_hash, password)

    @staticmethod
    def get_user_by_email(email):
        users_ref = db.collection("users").where("email", "==", email).get()
        if users_ref:
            user_data = users_ref[0].to_dict()
            return User(**user_data)
        return None

    def save_to_firestore(self):
        user_data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "oauth_github": self.oauth_github,
        }
        db.collection("users").document(self.id).set(user_data)

@login_manager.user_loader
def user_loader(id):
    """ Load user from Firestore instead of SQLAlchemy """
    user_data = db.collection("users").document(id).get()
    if user_data.exists:
        return User(**user_data.to_dict())
    return None
