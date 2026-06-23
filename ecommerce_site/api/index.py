from api._utils import json_response


def handler(request):
    return json_response({"status": "API is running"})
