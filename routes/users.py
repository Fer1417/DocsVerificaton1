# routes/users.py

from flask import Blueprint, jsonify
from db import mysql

bp = Blueprint('users', __name__, url_prefix='/api')

@bp.route('/users')
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, 
               CONCAT(nombre, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo, 
               curp, rfc 
        FROM usuarios
    """)
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)
