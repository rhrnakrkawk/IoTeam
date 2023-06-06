from routes.tables import tables_schema
from models import Tables
from sqlalchemy.orm import Session 
from sqlalchemy import and_,or_ 
from datetime import datetime
import pytz
utc_now = datetime.now(pytz.utc)
korea_timezone = pytz.timezone('Asia/Seoul')
def get_table_list(db:Session):
    table_list = db.query(Tables).all()
    total = len(table_list)
    return total,table_list

def get_table(db:Session, table_id:int):
    table = db.query(Tables).filter(table_id==table_id).first()
    return table

def create_table(db:Session, table_create:tables_schema.TableCreate):
    db_table = Tables(
                    table_id=table_create.table_id,  
                    customer_count=table_create.customer_count,
                    total_price=table_create.total_price,
                    table_time=datetime.now(pytz.utc).astimezone(korea_timezone).strftime("%Y-%m-%d")
                    )
    db.add(db_table)
    db.commit()
    
def update_table(db:Session, table_id:int,table_update:tables_schema.TableUpdate):
    db_table = db.query(Tables).filter(table_id==table_id).first()
    
    db_table.table_id = table_update.table_id
    db_table.customer_count = table_update.customer_count
    db_table.total_price = table_update.total_price
    db.add(db_table)
    db.commit()
        

def delete_table(db:Session,table_id:int):
    db_table = db.query(Tables).filter(table_id == table_id)
    db.delete(db_table)
    db.commit()
    
def pay_table(db:Session,table_id:int):
    db_table = db.query(Tables).filter(table_id == table_id).first()
    if db_table.is_paid == False:
        db_table.is_paid = True
        db.add(db_table)
        db.commit()
    else:
        raise Exception("이미 결제된 테이블입니다.")