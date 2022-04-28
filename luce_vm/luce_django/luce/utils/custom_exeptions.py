from rest_framework.views import exception_handler
from rest_framework.response import Response
import utils.utils as utils

STANDARD_RESPONSE = {
    "error": {
        "code": 400,
        "message": "message",
        "status": "ERROR",
        "details": [
            {
                "reason": "reason"
            }
        ]
    },
    "data": {}
}


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    _response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if _response is not None:
        details = _response.data["detail"]
        response = STANDARD_RESPONSE
        response["error"]["code"] = _response.status_code
        response["error"]["details"] = [details]
        _response = {"body": response, "status": response["error"]["code"]}

    print(_response)
    return _response


def blockchain_exception(tx_receipt, receipts=[None]):
    error = utils.format_error_blockchain(tx_receipt)
    response = STANDARD_RESPONSE
    response["error"]["code"] = 400
    response["error"]["message"] = "blockchain error"
    response["error"]["status"] = "ERROR"
    response["error"]["details"] = error
    response["data"]["transaction receipts"] = receipts
    print(response)
    return {"body": response, "status": response["error"]["code"]}


def validation_exeption(serializer):
    error = utils.format_errors(serializer.errors)
    response = STANDARD_RESPONSE
    response["error"]["code"] = 400
    response["error"]["message"] = "validation error"
    response["error"]["status"] = "ERROR"
    response["error"]["details"] = error
    return {"body": response, "status": response["error"]["code"]}


def custom_message(message):
    response = STANDARD_RESPONSE
    response["error"]["code"] = 400
    response["error"]["message"] = "validation error"
    response["error"]["status"] = "ERROR"
    response["error"]["details"] = message
    return {"body": response, "status": response["error"]["code"]}
