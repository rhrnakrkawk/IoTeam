from sqlalchemy.orm import Session
from sqlalchemy import or_,and_
from models import Orders,Foods,Tables,Stocks,Receipts
from routes.orders import orders_schema
from datetime import datetime
import pytz


utc_now = datetime.now(pytz.utc)
korea_timezone = pytz.timezone('Asia/Seoul')

def get_orders_list(db:Session):
    orders_list = db.query(Orders).all()
    total = db.query(Orders).count()
    
    return total, orders_list

def get_order(db:Session, table_id:int):
    order = db.query(Orders).filter(table_id == table_id)
    return order

def create_order(db: Session, order_create: orders_schema.OrdersCreate):
    table_id = order_create.table_id
    menus = order_create.menus

    db_table = db.query(Tables).filter(table_id == table_id).first()
    if db_table is None:
        raise ValueError("해당 테이블이 존재하지 않습니다.")

    total_price = 0

    for menu in menus:
        food_name = menu["food_name"]
        amount = menu["amount"]

        db_food = db.query(Foods).filter(Foods.name == food_name).first()
        if db_food is None:
            raise ValueError(f"해당 음식({food_name})이 존재하지 않습니다.")

        # 해당 음식의 레시피를 가져옴
        db_receipts = db.query(Receipts).filter(Receipts.food_name == food_name).all()
        # 해당 음식의 레시피의 개수를 가져옴
        db_receipts_cnt = len(db_receipts)
        cnt = 0
        # 해당 음식의 레시피의 개수만큼 반복
        for receipt in db_receipts:
            db_stock = db.query(Stocks).filter(Stocks.name == receipt.name).first()
            if db_stock is None:
                raise ValueError(f"해당 음식({food_name})의 재료({receipt.name})의 재고가 존재하지 않습니다.")
            cnt += 1
        
        if cnt != db_receipts_cnt:
            raise ValueError(f"해당 음식({food_name})의 재료의 개수가 일치하지 않습니다.")

        # 위의 조건 만족 시 주문 가능, 가격 계산
        total_price += amount * db_food.price

        # 재고 소모
        for receipt in db_receipts:
            db_stock = db.query(Stocks).filter(Stocks.name == receipt.name).first()
            db_stock.amount -= receipt.amount * amount
            db.add(db_stock)

        # 주문 생성
        db_order = Orders(table_id=table_id, menu=food_name, amount=amount, order_time=datetime.now(pytz.utc).astimezone(korea_timezone).strftime("%Y-%m-%d"))
        db.add(db_order)
        
        # 음식 선호도 + 1
        db_food = db.query(Foods).filter(Foods.name == food_name).first()
        db_food.populate += amount
        db.add(db_food)
        

    print(db_table.total_price)
    db_table.total_price += total_price
    db.add(db_table)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    return {"message": "주문이 성공적으로 생성되었습니다."}

def call_order(db:Session,call:orders_schema.Call):
    db_table = db.query(Tables).filter(Tables.table_id == call.table_id).first()
    if db_table is None:
        raise ValueError("해당 테이블이 존재하지 않습니다.")
    db_order = Orders(table_id=call.table_id,call=call.call,content=call.content)
    db.add(db_order)
    db.commit()
    return {"message":"호출 완료"}
def update_order(db:Session, order_update:orders_schema.OrdersUpdate):
    db_order = db.query(Orders).filter(Orders.table_id == order_update.order_id).first()
    if db_order == None:
        raise ValueError("해당 주문이 존재하지 않습니다.")
    
    db_order.menu = order_update.menu
    db_order.amount = order_update.amount
    db.add(db_order)
    db.commit()
    
def delete_order(db:Session,id:orders_schema.OrdersDelete):
    db_order = db.query(Orders).filter(Orders.table_id == id)
    db.delete(db_order)
    db.commit()
    
def call_list(db:Session):
    db_call = db.query(Orders).filter(Orders.call == True).all()
    return db_call