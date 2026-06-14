from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash, verify_password
from app.utils.exceptions import UserNotFound, InvalidCredentials
from app.models.saldo import Saldo

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            role=user_data.role
        )
        db.add(db_user)
        db.flush()
        
        # Create wallet (saldo) for new user
        saldo = Saldo(user_id=db_user.id, balance=0.0)
        db.add(saldo)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise UserNotFound()
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFound()
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentials()
        return user
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()
