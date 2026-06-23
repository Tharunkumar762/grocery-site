from ._db import get_db
from ._utils import get_json_body, json_response


def handler(request):
    if request.method != "POST":
        return json_response({"success": False, "message": "Method not allowed"}, 405)

    data = get_json_body(request)
    if not data or not data.get("email") or not data.get("password"):
        return json_response({"success": False, "message": "Missing required fields"}, 400)

    with get_db() as db:
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (data["email"], data["password"]),
        ).fetchone()

    if user:
        return json_response(
            {
                "success": True,
                "user_id": user["id"],
                "username": user["username"],
            }
        )

    return json_response({"success": False, "message": "Invalid credentials"}, 401)
