from fastapi import HTTPException, status

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
OBJECT_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Object not found",
    headers={"WWW-Authenticate": "Bearer"},
)
