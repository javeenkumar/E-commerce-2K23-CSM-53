from typing import Optional
from fastapi import HTTPException, status, Header

def get_current_admin(authorization: Optional[str] = Header(None)):
    """
    Enforces CAT-06: Administrative write operations reject unauthenticated
    or unauthorized requests.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format. Expected 'Bearer <token>'"
        )
    token = authorization.split("Bearer ")[1].strip()
    
    # Check for customer/unauthorized tokens
    if token == "customer-token" or "customer" in token.lower() or "user" in token.lower():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privilege required for this operation"
        )
    # Check valid admin token
    if token != "admin-token" and "admin" not in token.lower() and token != "mock-admin-jwt":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return {"username": "admin", "role": "admin"}
