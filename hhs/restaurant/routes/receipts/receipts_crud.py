from routes.receipts import receipts_schema
from models import Receipts
from sqlalchemy.orm import Session

def get_receipts_list(db:Session):
    
    receipts_list = db.query(Receipts).all()
    total = db.query(Receipts).count()
    
    return total,receipts_list

def get_receipts(db:Session, receipts_name:str):
    receipts = db.query(Receipts).filter(Receipts.food_name == receipts_name).all()
    return receipts

def create_receipts(db:Session, receipts_create:receipts_schema.ReceiptsCreate):
    ingredient = receipts_create.content
    for k,v in ingredient.items():
        db_receipts = Receipts(
                                food_name = receipts_create.food_name,
                                name = k,
                                amount = v
                                )
        db.add(db_receipts)
    db.commit()
    
def delete_receipts(db:Session, receipts_id:int):
    db_receipts = db.query(Receipts).filter(Receipts.id == receipts_id)
    if db_receipts is None:
        raise ValueError("해당 레시피가 존재하지 않습니다.")
    db.delete(db_receipts)
    db.commit()
