from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.arisan import Arisan, ArisanMember, ArisanStatus, MemberStatus
from app.models.transaksi import Transaksi
from app.schemas.arisan import ArisanCreate
from app.utils.exceptions import ArisanNotFound, ArisanFull, AlreadyMember, UnauthorizedOperation

class ArisanService:
    @staticmethod
    def create_arisan(db: Session, host_id: int, arisan_data: ArisanCreate) -> Arisan:
        db_arisan = Arisan(
            host_id=host_id,
            name=arisan_data.name,
            description=arisan_data.description,
            jumlah_peserta=arisan_data.jumlah_peserta,
            patungan_per_minggu=arisan_data.patungan_per_minggu,
            status=ArisanStatus.ACTIVE
        )
        db.add(db_arisan)
        db.commit()
        db.refresh(db_arisan)
        return db_arisan
    
    @staticmethod
    def get_arisan(db: Session, arisan_id: int) -> Arisan:
        arisan = db.query(Arisan).filter(Arisan.id == arisan_id).first()
        if not arisan:
            raise ArisanNotFound()
        return arisan
    
    @staticmethod
    def get_all_arisans(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Arisan).offset(skip).limit(limit).all()
    
    @staticmethod
    def join_arisan(db: Session, arisan_id: int, user_id: int, saldo_awal: float) -> ArisanMember:
        arisan = ArisanService.get_arisan(db, arisan_id)
        
        # Check if arisan is full
        member_count = db.query(func.count(ArisanMember.id)).filter(
            ArisanMember.arisan_id == arisan_id,
            ArisanMember.status == MemberStatus.ACTIVE
        ).scalar()
        
        if member_count >= arisan.jumlah_peserta:
            raise ArisanFull()
        
        # Check if already member
        existing = db.query(ArisanMember).filter(
            ArisanMember.arisan_id == arisan_id,
            ArisanMember.user_id == user_id,
            ArisanMember.status == MemberStatus.ACTIVE
        ).first()
        
        if existing:
            raise AlreadyMember()
        
        db_member = ArisanMember(
            arisan_id=arisan_id,
            user_id=user_id,
            saldo_awal=saldo_awal,
            status=MemberStatus.ACTIVE
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return db_member
    
    @staticmethod
    def get_arisan_members(db: Session, arisan_id: int):
        return db.query(ArisanMember).filter(ArisanMember.arisan_id == arisan_id).all()
    
    @staticmethod
    def get_user_arisans(db: Session, user_id: int):
        return db.query(ArisanMember).filter(ArisanMember.user_id == user_id).all()
