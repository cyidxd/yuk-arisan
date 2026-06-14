from pydantic import BaseModel
from datetime import datetime
from app.models.transaksi import TipTransaksi, StatusTransaksi

class TransaksiResponse(BaseModel):
    id: int
    arisan_id: int
    from_user_id: int
    to_user_id: int
    amount: float
    tipe: TipTransaksi
    status: StatusTransaksi
    keterangan: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class KomisiResponse(BaseModel):
    id: int
    transaksi_id: int
    arisan_id: int
    amount: float
    collected_at: datetime
    
    class Config:
        from_attributes = True
