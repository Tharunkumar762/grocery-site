from api._db import get_db
from api._utils import json_response


def handler(request):
    if request.method != "GET":
        return json_response({"success": False, "message": "Method not allowed"}, 405)

    with get_db() as db:
        users = db.execute("SELECT id, username, email FROM users").fetchall()

    return json_response([dict(user) for user in users])
