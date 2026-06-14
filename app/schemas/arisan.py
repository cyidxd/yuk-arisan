from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.arisan import ArisanStatus, MemberStatus

class ArisanBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    jumlah_peserta: int = Field(..., ge=2, le=100)
    patungan_per_minggu: float = Field(..., gt=0)

class ArisanCreate(ArisanBase):
    pass

class ArisanMemberResponse(BaseModel):
    id: int
    user_id: int
    saldo_awal: float
    status: MemberStatus
    sudah_dapat_giliran: bool
    joined_at: datetime
    
    class Config:
        from_attributes = True

class ArisanResponse(ArisanBase):
    id: int
    host_id: int
    status: ArisanStatus
    created_at: datetime
    updated_at: datetime
    members: Optional[List[ArisanMemberResponse]] = []
    
    class Config:
        from_attributes = True

class ArisanDetailResponse(ArisanResponse):
    jumlah_anggota: int
    total_dana_terkumpul: float
