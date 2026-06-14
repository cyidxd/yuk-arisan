from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base

class UserRole(str, Enum):
    ADMIN = "admin"  # Admin system
    HOST = "host"    # Host arisan
    MEMBER = "member"  # Member arisan

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    arisans_hosted = relationship("Arisan", back_populates="host", foreign_keys="Arisan.host_id")
    arisan_memberships = relationship("ArisanMember", back_populates="user")
    saldo = relationship("Saldo", uselist=False, back_populates="user")
    transaksi_from = relationship("Transaksi", foreign_keys="Transaksi.from_user_id", back_populates="from_user")
    transaksi_to = relationship("Transaksi", foreign_keys="Transaksi.to_user_id", back_populates="to_user")
    
    def __repr__(self):
        return f"<User {self.username}>"
