from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.helpers import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def auth_middleware(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)

    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return int(payload["sub"])