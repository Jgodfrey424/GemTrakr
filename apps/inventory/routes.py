from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required, current_user
from google.cloud import firestore
from werkzeug.utils import secure_filename
from firebase_admin import firestore
import os
import uuid
import logging
import qrcode
from io import BytesIO

inventory_bp = Blueprint('inventory', __name__)

db = firestore.Client()

@inventory_bp.route('/add_item', methods=['POST'])
@login_required
def add_item():
    try:
        data = request.form
        picture_file = request.files.get('file')
        picture_path = ''
        
        if picture_file:
            uploads_dir = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            filename = f"{data['barcode'][-4:]}.jpg"
            picture_path = os.path.join(uploads_dir, filename)
            picture_file.save(picture_path)
        
        item_data = {
            'item_id': data['item_id'],
            'title': data['title'],
            'description': data['description'],
            'barcode': data['barcode'],
            'picture_path': picture_path,
            'cost': float(data['cost']),
            'price': float(data['price']),
            'quantity': int(data['quantity']),
            'item_location': data['item_location']
        }
        
        db.collection('inventory').document(item_data['item_id']).set(item_data)
        return jsonify(success=True, message="Item added successfully")
    except Exception as e:
        logging.error(f"Error adding item: {e}")
        return jsonify(success=False, message="Error adding item"), 500

@inventory_bp.route('/list_inventory', methods=['GET'])
@login_required
def list_inventory():
    try:
        inventory_ref = db.collection('inventory')
        docs = inventory_ref.stream()
        items = [doc.to_dict() for doc in docs]
        return jsonify(items)
    except Exception as e:
        logging.error(f"Failed to retrieve items: {e}")
        return jsonify({"error": str(e)}), 500

@inventory_bp.route('/delete_item/<item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    try:
        db.collection('inventory').document(item_id).delete()
        return jsonify(success=True, message="Item deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting item {item_id}: {e}")
        return jsonify(success=False, message="Error deleting item"), 500

@inventory_bp.route('/generate_qr_code/<data>', methods=['GET'])
@login_required
def generate_qr_code(data):
    if len(data) > 200:
        return "Data too long for QR code", 400
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_bytes = BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')
