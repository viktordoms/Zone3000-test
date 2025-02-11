from rest_framework import status
from rest_framework.response import Response


def error_not_found(error: str, code = status.HTTP_404_NOT_FOUND) -> Response:
    """ Default not found error response"""
    return Response(
        data={"result": error},
        status=code,
    )

def error_bad_request(error: str, code = status.HTTP_400_BAD_REQUEST) -> Response:
    """ Default bad request error response"""
    return Response(
        data={"result": error},
        status=code,
    )

def success_response(message: str, code = status.HTTP_200_OK) -> Response:
    """ Default success response """
    return Response(
        data={"result": message},
        status=code,
    )