from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Foods, Receipts, Orders, Stocks, Tables
router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
)

# 인기 메뉴 조회
@router.get("/populate",summary="인기 메뉴 조회")
def get_populate_food(db:Session=Depends(get_db)):
    db_food = db.query(Foods).all()
    populate_list = {}
    for food in db_food:
        populate_list[food.name] = food.populate
        
    if not populate_list:
        return "No Data"
    
    return {
        "Popular": max(populate_list, key=populate_list.get),
        "Food": populate_list
        }
    

# 특정 음식의 인기도 조회
@router.get("/populate/{food_name}",summary="특정 음식의 인기도 조회")
def get_populate_food(db:Session=Depends(get_db), food_name:str=None):
    db_food = db.query(Foods).filter(Foods.name == food_name).first()
    if db_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 음식이 존재하지 않습니다.")
    return db_food.populate

# 사장의 PICK 메뉴 조회
@router.get("/pick",summary="사장의 PICK 메뉴 조회")
def get_pick_food(db:Session=Depends(get_db)):
    db_food = db.query(Foods).filter(Foods.pick == True).all()
    
    if not db_food:
        return "No Pick Data"
    
    return db_food
# 사장의 PICK 메뉴 설정
@router.post("/pick",summary="사장의 PICK 메뉴 추가")
def set_pick_menu(db:Session=Depends(get_db), food_name:str=None):
    db_food = db.query(Foods).filter(Foods.name == food_name).first()
    
    if db_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 음식이 존재하지 않습니다.")
    
    db_food.pick = True
    db.commit()
    return "사장의 PICK 메뉴로 추가되었습니다."

# 사장의 PICK 메뉴 취소
@router.delete("/pick",summary="사장의 PICK 메뉴 취소")
def delete_pick_menu(db:Session=Depends(get_db), food_name:str=None):
    db_food = db.query(Foods).filter(Foods.name == food_name).first()
    
    if db_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 음식이 존재하지 않습니다.")
    
    db_food.pick = False
    db.commit()
    return "사장의 PICK 메뉴에서 삭제되었습니다."

# 일간 매출 확인
@router.get("/sales/daily", summary="일간 매출 확인")
def get_daily_sales(db: Session = Depends(get_db)):
    db_order = db.query(Orders).all()
    daily_sales = {}

    for order in db_order:
        order_time = order.order_time
        ## 임시. 삭제 예정
        if order_time is None:
            continue
        if order.menu is None or order.amount is None:
            continue
        order_date = order_time.date()  # 시간 정보 제외, 날짜 정보만 추출
        order_date_str = order_date.strftime("%Y-%m-%d")  # 날짜를 문자열로 변환
        food_price = db.query(Foods).filter(Foods.name == order.menu).first().price
        if order_date_str in daily_sales:
            daily_sales[order_date_str] += order.amount * food_price
        else:
            daily_sales[order_date_str] = order.amount * food_price

    if not daily_sales :
        return "No Data"

    return daily_sales

@router.get("/sales/monthly", summary="월간 매출 확인")
def get_daily_sales(db: Session = Depends(get_db)):
    db_order = db.query(Orders).all()
    daily_sales = {}

    for order in db_order:
        order_time = order.order_time
        if order_time is None:
            continue
        if order.menu is None or order.amount is None:
            continue 
        order_date = order_time.date()  # 시간 정보 제외, 날짜 정보만 추출
        order_date_str = order_date.strftime("%Y-%m")  # 날짜를 문자열로 변환
        food_price = db.query(Foods).filter(Foods.name == order.menu).first().price
        if order_date_str in daily_sales:
            
            daily_sales[order_date_str] += order.amount * food_price
        else:
            
            daily_sales[order_date_str] = order.amount * food_price

    if not daily_sales:
        return "No Data"

    return daily_sales

@router.get("/customer/total", summary="총 방문자 수 확인")
def get_daily_sales(db: Session = Depends(get_db)):
    db_table = db.query(Tables).all()
    total_customer = 0
    
    for table in db_table:
        total_customer += table.customer_count
    
    return "총 방문자 수는 " + str(total_customer) + "명 입니다."

@router.get("/customer/daily", summary="일간 방문자 수 확인")
def get_daily_sales(db: Session = Depends(get_db)):
    db_table = db.query(Tables).all()
    daily_customer = {}
    
    for table in db_table:
        table_time = table.table_time
        if table_time is None:
            continue

        table_date = table_time.date()
        order_date_str = table_date.strftime("%Y-%m-%d")  # 날짜를 문자열로 변환
        
        if order_date_str in daily_customer:
            daily_customer[order_date_str] += table.customer_count
        else:
            daily_customer[order_date_str] = table.customer_count
    if not daily_customer:
        return "No Data"
    else:
        return daily_customer
    
@router.get("/customer/monthly", summary="월간 방문자 수 확인")
def get_daily_sales(db: Session = Depends(get_db)):
    db_table =db.query(Tables).all()
    daily_customer = {}
    
    for table in db_table:
        table_time = table.table_time
        if table_time is None:
            continue

        table_date = table_time.date()
        order_date_str = table_date.strftime("%Y-%m")  # 날짜를 문자열로 변환
        
        if order_date_str in daily_customer:
            daily_customer[order_date_str] += table.customer_count
        else:
            daily_customer[order_date_str] = table.customer_count
    if not daily_customer:
        return "No Data"
    else:
        return daily_customer