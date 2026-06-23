from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)
CORS(app)

# Serve main page on root
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

# Serve other frontend files from the project root
@app.route("/<path:path>")
def static_file(path):
    return send_from_directory(BASE_DIR, path)

# ---------- DATABASE (ABSOLUTE PATH) ----------
DATABASE = os.path.join(BASE_DIR, "database.db")
DATABASE = os.path.join(BASE_DIR, "database.db")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- CREATE TABLES ----------
with get_db() as db:
    db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product TEXT,
        status TEXT
    )
    """)

# ---------- REGISTER ----------
@app.route("/register", methods=["POST"])
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    print("REGISTER DATA:", data)  # DEBUG

    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (data["username"], data["email"], data["password"])
            )

        return jsonify(success=True, message="User registered")

    except sqlite3.IntegrityError as e:
        print("REGISTER ERROR:", e)
        return jsonify(success=False, message="Email already exists"), 400

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    print("LOGIN DATA:", data)  # DEBUG

    with get_db() as db:
        users = db.execute("SELECT * FROM users").fetchall()
        print("USERS IN DB:", [dict(u) for u in users])  # DEBUG

        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (data["email"], data["password"])
        ).fetchone()

    print("MATCHED USER:", user)  # DEBUG

    if user:
        return jsonify(
            success=True,
            user_id=user["id"],
            username=user["username"]
        )

    return jsonify(success=False, message="Invalid credentials"), 401

# ---------- ORDER ----------
@app.route("/order", methods=["POST"])
@app.route("/api/order", methods=["POST"])
def order():
    data = request.json

    with get_db() as db:
        db.execute(
            "INSERT INTO orders(user_id,product,status) VALUES (?,?,?)",
            (data["user_id"], data["product"], "Pending")
        )

    return jsonify(success=True, message="Order placed")

# ---------- ADMIN LOGIN ----------
@app.route("/admin/login", methods=["POST"])
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.json

    # simple hardcoded admin (for now)
    if data["email"] == "admin@gmail.com" and data["password"] == "admin123":
        return jsonify(success=True)

    return jsonify(success=False), 401


# ---------- GET ALL USERS ----------
@app.route("/admin/users", methods=["GET"])
@app.route("/api/admin/users", methods=["GET"])
def get_users():
    with get_db() as db:
        users = db.execute("SELECT id, username, email FROM users").fetchall()

    return jsonify([dict(u) for u in users])


# ---------- GET ALL ORDERS ----------
@app.route("/admin/orders", methods=["GET"])
@app.route("/api/admin/orders", methods=["GET"])
def get_orders():
    with get_db() as db:
        orders = db.execute("""
            SELECT orders.id, users.username, orders.product, orders.status
            FROM orders
            JOIN users ON orders.user_id = users.id
        """).fetchall()

    return jsonify([dict(o) for o in orders])


# ---------- APPROVE ORDER ----------
@app.route("/admin/order/approve", methods=["POST"])
@app.route("/api/admin/order/approve", methods=["POST"])
def approve_order():
    data = request.json

    with get_db() as db:
        db.execute(
            "UPDATE orders SET status='Approved' WHERE id=?",
            (data["order_id"],)
        )

    return jsonify(success=True)


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
