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
    db_receipts = db.query(Receipts).get(receipts_id)
    db.delete(db_receipts)
    db.commit()
