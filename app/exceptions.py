from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = "Internal Server Error"

    def __init__(self, **kwargs) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class ServerError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str) -> None:
        self.DETAIL = detail
        super().__init__()


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class CustomerNotFound(NotFound):
    DETAIL = "Customer not found"


class InvalidPasswordOrEmail(DetailedHTTPException):
    DETAIL = "Invalid password or email"
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED


class CustomerAlreadyExists(DetailedHTTPException):
    DETAIL = "Customer already exists"
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
