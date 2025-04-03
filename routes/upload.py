import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.ocr import validate_document
from models.user import mysql

bp = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    user_id = request.form.get("user_id")

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT curp, rfc, imss FROM usuarios WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        return jsonify({"error": "User not found"}), 404

    validation_results, extracted_data = validate_document(file_path, user_data)

    if validation_results['curp'] or validation_results['rfc'] or validation_results['imss']:
        cursor.execute("""
            UPDATE usuarios 
            SET curp = %s, rfc = %s, imss = %s
            WHERE id = %s
        """, (extracted_data['curp'], extracted_data['rfc'], extracted_data['imss'], user_id))
        mysql.connection.commit()

    return jsonify({
        "message": "Document processed successfully",
        "validation_results": validation_results,
        "extracted_data": extracted_data
    })
