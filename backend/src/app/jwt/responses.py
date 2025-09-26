from rest_framework.response import Response


def custom_response(
    success: bool, status_code: int, message: str, data=None, errors=None
):
    payload = {
        "success": success,
        "status": status_code,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    if errors is not None:
        payload["errors"] = errors

    return Response(payload, status=status_code)
