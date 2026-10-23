from fastapi import HTTPException, status

class Unauthed(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password")

class EmailTaken(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

class UserNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

class TripNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

class NotTripMember(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="You aren't trip member")

class WrongTripPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong trip password")

class TooManyAttempts(HTTPException):
    def __init__(self, retry_after: int):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many attempts, try it later",
                         headers={"Retry-After": str(max(retry_after, 1))})