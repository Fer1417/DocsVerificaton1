<<<<<<< HEAD
def create_tables(mysql):
    cursor = mysql.connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido_paterno VARCHAR(100) NOT NULL,
        apellido_materno VARCHAR(100),
        curp VARCHAR(18) UNIQUE,
        rfc VARCHAR(13) UNIQUE,
        imss VARCHAR(11) UNIQUE,
        constancia_fiscal VARCHAR(255)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS constancias_cursos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        nombre_curso VARCHAR(255) NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cedulas_profesionales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        numero_cedula VARCHAR(20) NOT NULL UNIQUE,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    )''')

    mysql.connection.commit()
    cursor.close()
=======
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
>>>>>>> eb11466 (Se cambio la isntancia y se esta modificando el login así como la interfaz donde se ve la información)
