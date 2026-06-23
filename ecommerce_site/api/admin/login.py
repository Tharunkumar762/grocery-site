from .._db import get_db
from .._utils import get_json_body, json_response


def handler(request):
    if request.method != "POST":
        return json_response({"success": False, "message": "Method not allowed"}, 405)

    data = get_json_body(request)
    if not data or not data.get("email") or not data.get("password"):
        return json_response({"success": False, "message": "Missing required fields"}, 400)

    if data["email"] == "admin@gmail.com" and data["password"] == "admin123":
        return json_response({"success": True})

    return json_response({"success": False, "message": "Invalid admin credentials"}, 401)
