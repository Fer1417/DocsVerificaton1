from flask import Flask, render_template
from config import Config
from db import mysql
from routes.upload import bp as upload_bp
from routes.users import bp as users_bp
from routes.auth import bp as auth_bp

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

app.register_blueprint(auth_bp)  
app.register_blueprint(upload_bp)
app.register_blueprint(users_bp)

@app.route("/")
def index():
    return "<h1>Servidor Flask corriendo</h1>"

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/login_dashboard.html")
def login():
    return render_template("login_dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
