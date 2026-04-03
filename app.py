# app.py — Flask app intencionalmente vulnerable
# SOLO para aprendizaje, nunca en producción

from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import subprocess

app = Flask(__name__)

# Vuln 1: secreto hardcodeado (SAST lo detecta)
SECRET_KEY = "super-secret-key-12345"
DB_PASSWORD = "admin123"

# Vuln 2: SQL Injection (SAST + DAST lo detectan)
@app.route("/user")
def get_user():
    username = request.args.get("name")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # INSEGURO: concatenación directa
    query = f"SELECT * FROM users WHERE name = '{username}'"
    cursor.execute(query)
    return str(cursor.fetchall())

# Vuln 3: XSS (DAST lo detecta)
@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    # INSEGURO: input directo en template
    return render_template_string(f"<h1>Hola {name}</h1>")

# Vuln 4: Command injection
@app.route("/ping")
def ping():
    host = request.args.get("host")
    # INSEGURO: shell=True con input del usuario
    result = subprocess.run(
        f"ping -c 1 {host}", shell=True, capture_output=True
    )
    return result.stdout.decode()

# Health check para DAST
@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)