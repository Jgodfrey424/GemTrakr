# -*- encoding: utf-8 -*-
"""
Modified from AppSeed.us - Now using Firestore instead of SQLAlchemy
"""

import os
from flask_minify import Minify
from sys import exit
from apps import create_app
from apps.firebase_init import db  # Ensure Firestore is initialized
from apps.config import config_dict  # Un-commented to load the configuration

# WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]  # FIXED: Now correctly referencing config_dict
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production]')

# Create Flask app
app = create_app(app_config)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info(f"DEBUG       = {DEBUG}")
    app.logger.info(f"ASSETS_ROOT = {app_config.ASSETS_ROOT}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

