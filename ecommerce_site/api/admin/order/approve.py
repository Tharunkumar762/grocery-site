from api._db import get_db
from api._utils import get_json_body, json_response


def handler(request):
    if request.method != "POST":
        return json_response({"success": False, "message": "Method not allowed"}, 405)

    data = get_json_body(request)
    if not data or not data.get("order_id"):
        return json_response({"success": False, "message": "Missing required fields"}, 400)

    with get_db() as db:
        db.execute(
            "UPDATE orders SET status='Approved' WHERE id=?",
            (data["order_id"],),
        )

    return json_response({"success": True, "message": "Order approved"})
