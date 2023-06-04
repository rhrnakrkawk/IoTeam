from sqlalchemy.orm import Session
from sqlalchemy import or_,and_
from models import Orders,Foods,Tables,Stocks,Receipts
from routes.orders import orders_schema
from datetime import datetime
def get_orders_list(db:Session):
    orders_list = db.query(Orders).all()
    total = db.query(Orders).count()
    
    return total, orders_list

def get_order(db:Session, table_id:int):
    order = db.query(Orders).get(table_id)
    return order

def create_order(db: Session, order_create: orders_schema.OrdersCreate):
    table_id = order_create.table_id
    menus = order_create.menus

    db_table = db.query(Tables).get(table_id)
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
        db_receipts_cnt = db.query(Receipts).filter(Receipts.food_name == food_name).all().count()
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

        # 재고 소진
        db_stock.amount -= amount
        db.add(db_stock)

        # 주문 생성
        order_time = datetime.now()
        
        db_order = Orders(table_id=table_id, menu=food_name, amount=amount, order_time=order_time)
        db.add(db_order)
        
        # 음식 선호도 + 1
        db_food = db.query(Foods).filter(Foods.name == food_name).first()
        db_food.populate += 1
        db.add(db_food)
        

    
    db_table.total_price += total_price
    db.add(db_table)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    return {"message": "주문이 성공적으로 생성되었습니다."}
    
def update_order(db:Session,id:int, order_update:orders_schema.OrdersUpdate):
    db_order = db.query(Orders).get(id)
    db_order.menu = order_update.menu
    db_order.amount = order_update.amount
    db.add(db_order)
    db.commit()
    
def delete_order(db:Session,id:orders_schema.OrdersDelete):
    db_order = db.query(Orders).get(id)
    db.delete(db_order)
    db.commit()