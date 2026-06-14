from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import decode_token
from app.models.user import User
from app.utils.exceptions import InvalidCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise InvalidCredentials()
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise InvalidCredentials()
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise InvalidCredentials()
    
    return user
