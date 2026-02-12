from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.auth import decode_access_token
from app.db.database import get_db
from app.db.models.users import User

security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload


def get_current_user(
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
) -> User:

    user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not user:
        raise HTTPException(401, "User not found")

    return user
