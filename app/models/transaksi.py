from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database import Base

class TipTransaksi(str, Enum):
    TAGIHAN = "tagihan"  # Weekly billing
    PAYOUT = "payout"    # Winner payout
    KOMISI = "komisi"    # Admin commission
    TOPUP = "topup"      # Manual top-up

class StatusTransaksi(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Transaksi(Base):
    __tablename__ = "transaksis"
    
    id = Column(Integer, primary_key=True, index=True)
    arisan_id = Column(Integer, ForeignKey("arisans.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    tipe = Column(SQLEnum(TipTransaksi), nullable=False)
    status = Column(SQLEnum(StatusTransaksi), default=StatusTransaksi.PENDING, nullable=False)
    keterangan = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    arisan = relationship("Arisan", back_populates="transaksi")
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="transaksi_from")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="transaksi_to")
    komisi = relationship("Komisi", back_populates="transaksi", uselist=False)
    
    def __repr__(self):
        return f"<Transaksi {self.id} {self.tipe}>"

class Komisi(Base):
    __tablename__ = "komisis"
    
    id = Column(Integer, primary_key=True, index=True)
    transaksi_id = Column(Integer, ForeignKey("transaksis.id"), nullable=False, unique=True)
    arisan_id = Column(Integer, ForeignKey("arisans.id"), nullable=False)
    amount = Column(Float, nullable=False)  # 5% dari payout
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    transaksi = relationship("Transaksi", back_populates="komisi")
    arisan = relationship("Arisan", back_populates="komisi")
    
    def __repr__(self):
        return f"<Komisi {self.id} amount={self.amount}>"
