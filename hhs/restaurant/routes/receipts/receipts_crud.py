from routes.receipts import receipts_schema
from models import Receipts
from sqlalchemy.orm import Session

def get_receipts_list(db: Session):
    """
    모든 레시피 정보 출력

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        int: 레시피의 총 개수
        list: 레시피 목록
    """
    receipts_list = db.query(Receipts).all()
    total = db.query(Receipts).count()
    return total, receipts_list


def get_receipts(db: Session, receipts_name: str):
    """
    특정 음식의 레시피 정보 출력

    Args:
        db (Session): SQLAlchemy 세션 객체
        receipts_name (str): 조회할 음식의 이름

    Returns:
        list: 레시피 목록
    """
    receipts = db.query(Receipts).filter(Receipts.food_name == receipts_name).all()
    return receipts


def create_receipts(db: Session, receipts_create: receipts_schema.ReceiptsCreate):
    """
    새로운 레시피 추가

    Args:
        db (Session): SQLAlchemy 세션 객체
        receipts_create (ReceiptsCreate): 레시피 생성에 필요한 정보
    """
    ingredient = receipts_create.content
    for k, v in ingredient.items():
        db_receipts = Receipts(
            food_name=receipts_create.food_name,
            name=k,
            amount=v,
        )
        db.add(db_receipts)
    db.commit()


def delete_receipts(db: Session, receipts_id: int):
    """
    레시피 삭제

    Args:
        db (Session): SQLAlchemy 세션 객체
        receipts_id (int): 삭제할 레시피의 ID
    """
    db_receipts = db.query(Receipts).filter(Receipts.id == receipts_id)
    if db_receipts is None:
        raise ValueError("해당 레시피가 존재하지 않습니다.")
    db.delete(db_receipts)
    db.commit()
