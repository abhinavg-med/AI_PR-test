from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# Hardcoded credentials (A02:2021-Cryptographic Failures)
DB_NAME = "users.db"
API_KEY = "12345-ABCDE-SECRET-KEY"  # Exposed API Key

# SQL Injection Vulnerability (A03:2021-Injection)
@app.route("/user", methods=["GET"])
def get_user():
    user_id = request.args.get("user_id")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}'"  # Vulnerable to SQL Injection
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    
    return str(result) if result else "No user found." 

# XSS Vulnerability (A07:2021-Identification and Authentication Failures)
@app.route("/comment", methods=["POST"])
def submit_comment():
    comment = request.form.get("comment")
    return f"User Comment: {comment}"  # No sanitization, allows script injection

# Insecure Direct Object Reference (IDOR) (A01:2021-Broken Access Control)
@app.route("/files", methods=["GET"])
def read_file():
    filename = request.args.get("file")
    with open(f"uploads/{filename}", "r") as file:  # Allows arbitrary file access
        return file.read()

if __name__ == "__main__":
    app.run(debug=True)  # Security Misconfiguration: debug mode enabled
