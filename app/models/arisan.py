from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base

class ArisanStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class MemberStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"

class Arisan(Base):
    __tablename__ = "arisans"
    
    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    jumlah_peserta = Column(Integer, nullable=False)  # Max participants
    patungan_per_minggu = Column(Float, nullable=False)  # Weekly contribution
    status = Column(SQLEnum(ArisanStatus), default=ArisanStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    host = relationship("User", back_populates="arisans_hosted", foreign_keys=[host_id])
    members = relationship("ArisanMember", back_populates="arisan", cascade="all, delete-orphan")
    transaksi = relationship("Transaksi", back_populates="arisan", cascade="all, delete-orphan")
    komisi = relationship("Komisi", back_populates="arisan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Arisan {self.name}>"

class ArisanMember(Base):
    __tablename__ = "arisan_members"
    
    id = Column(Integer, primary_key=True, index=True)
    arisan_id = Column(Integer, ForeignKey("arisans.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    saldo_awal = Column(Float, nullable=False)  # Initial balance when joining
    status = Column(SQLEnum(MemberStatus), default=MemberStatus.ACTIVE, nullable=False)
    sudah_dapat_giliran = Column(Boolean, default=False)  # Whether already received payout
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    arisan = relationship("Arisan", back_populates="members")
    user = relationship("User", back_populates="arisan_memberships")
    
    def __repr__(self):
        return f"<ArisanMember user={self.user_id} arisan={self.arisan_id}>"
