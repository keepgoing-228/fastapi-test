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
