import json


def get_json_body(request):
    if hasattr(request, "get_json"):
        data = request.get_json(silent=True)
        if data is not None:
            return data

    raw = getattr(request, "body", None)
    if raw is None:
        raw = getattr(request, "data", None)

    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")

    if not raw:
        return {}

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def json_response(payload, status_code=200):
    return {
        "statusCode": status_code,
        "body": json.dumps(payload),
        "headers": {
            "Content-Type": "application/json"
        }
    }
