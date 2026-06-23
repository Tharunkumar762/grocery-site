import sqlite3
from ._db import get_db
from ._utils import get_json_body, json_response


def handler(request):
    if request.method != "POST":
        return json_response({"success": False, "message": "Method not allowed"}, 405)

    data = get_json_body(request)
    if not data or not data.get("username") or not data.get("email") or not data.get("password"):
        return json_response({"success": False, "message": "Missing required fields"}, 400)

    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (data["username"], data["email"], data["password"]),
            )

        return json_response({"success": True, "message": "User registered"})
    except sqlite3.IntegrityError:
        return json_response({"success": False, "message": "Email already exists"}, 400)
