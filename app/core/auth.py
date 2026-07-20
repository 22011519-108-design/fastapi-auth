from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token"
)


def get_current_user_payload(
    token: str = Depends(oauth2_scheme)
) -> dict[str, Any]:

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    if payload.get("sub") is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload


def get_current_user(
    payload: dict[str, Any] = Depends(get_current_user_payload)
) -> str:
    return payload["sub"]


def get_current_user_id(
    payload: dict[str, Any] = Depends(get_current_user_payload)
) -> int:
    try:
        return int(payload["user_id"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain a valid user_id",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )
