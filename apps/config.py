import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

try:
    # Fetch Firebase key path securely from .env
    cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

    if not cred_path:
        raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY is not set in .env")

    # Ensure credentials exist before proceeding
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")

    logging.info("Initializing Firestore client securely...")

    # Prevent multiple initializations
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    logging.info("Firestore client initialized successfully.")

except Exception as e:
    logging.error(f"Failed to initialize Firestore: {e}")
    db = None  # Prevent breaking app if Firestore fails

# Flask Configuration
class Config:
    """ Set Flask configuration variables from environment variables """

    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Change this in production!
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # Firestore Configuration
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Static Assets
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')


class DebugConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Dictionary mapping environment names to config classes
config_dict = {
    'Debug': DebugConfig,
    'Production': ProductionConfig
}
