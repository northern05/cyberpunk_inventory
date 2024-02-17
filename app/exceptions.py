from fastapi import HTTPException


class BadDataFormat(HTTPException):
    def __init__(self, detail="Bad data format"):
        super().__init__(status_code=400, detail=detail)


class ContentNotFound(HTTPException):
    def __init__(self, detail="Content not found"):
        super().__init__(status_code=404, detail=detail)


class UserAlreadyExists(HTTPException):
    def __init__(self, detail="User already exists!"):
        super().__init__(status_code=400, detail=detail)


class Unauthorized(HTTPException):
    def __init__(self, detail="Unauthorize!"):
        super().__init__(status_code=401, detail=detail)
