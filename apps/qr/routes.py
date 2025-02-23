from flask import Blueprint, send_file, jsonify
from flask_login import login_required
import qrcode
from io import BytesIO

qr_bp = Blueprint('qr', __name__)

@qr_bp.route('/generate_qr_code/<data>', methods=['GET'])
@login_required
def generate_qr_code(data):
    if len(data) > 200:
        return jsonify(success=False, message="Data too long for QR code"), 400
    try:
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
    except Exception as e:
        return jsonify(success=False, message=f"Error generating QR code: {str(e)}"), 500
