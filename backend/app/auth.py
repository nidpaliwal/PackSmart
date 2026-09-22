from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-Admin-Token", auto_error=False)


def require_admin(token: str = Security(api_key_header)):
    if not token or token != settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin token",
        )
    return True
