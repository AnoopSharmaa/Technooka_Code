from rest_framework.response import Response


def success_response(
    message="Success",
    data=None,
    status_code=200
):

    response_data = {
        "success": True,
        "message": message,
        "data": data
    }

    return Response(response_data, status=status_code)


def error_response(
    message="Something went wrong",
    errors=None,
    status_code=400
):

    response_data = {
        "success": False,
        "message": message,
        "errors": errors
    }

    return Response(response_data, status=status_code)