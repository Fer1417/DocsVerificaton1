
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from db import mysql

bp = Blueprint('auth', __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, password FROM administradores WHERE email = %s", (email,))
        admin = cursor.fetchone()
        cursor.close()

        if admin and check_password_hash(admin["password"], password):
            session["admin_id"] = admin["id"]
            return redirect("/dashboard")
        else:
            flash("Acceso denegado")
            return redirect("/login")

    return render_template("login_dashboard.html")


@bp.route("/dashboard")
def dashboard():
    if "admin_id" not in session:
        return redirect(url_for("auth.login"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, apellido_paterno, apellido_materno, curp, rfc FROM usuarios")
    users = cursor.fetchall()
    cursor.close()

    return render_template("login_dashboard.html", users=users)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

