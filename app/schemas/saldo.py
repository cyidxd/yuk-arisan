from pydantic import BaseModel
from datetime import datetime

class SaldoResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    last_updated: datetime
    
    class Config:
        from_attributes = True

class SaldoUpdateRequest(BaseModel):
    amount: float
    keterangan: str
