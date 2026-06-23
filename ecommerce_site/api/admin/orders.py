from api._db import get_db
from api._utils import json_response


def handler(request):
    if request.method != "GET":
        return json_response({"success": False, "message": "Method not allowed"}, 405)

    with get_db() as db:
        orders = db.execute(
            """
            SELECT orders.id, users.username, orders.product, orders.status
            FROM orders
            JOIN users ON orders.user_id = users.id
            """
        ).fetchall()

    return json_response([dict(order) for order in orders])
