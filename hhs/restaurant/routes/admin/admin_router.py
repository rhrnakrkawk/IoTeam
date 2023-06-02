from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from routes.foods import foods_router
from routes.receipts import receipts_router
from routes.orders import orders_router
from routes.stocks import stocks_router
from routes.tables import tables_router
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
        "Most Popular Food": max(populate_list, key=populate_list.get),
        "Food Popularity": populate_list
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
    return {"msg":"사장의 PICK 메뉴로 추가되었습니다."}
# 사장의 PICK 메뉴 취소
@router.delete("/pick",summary="사장의 PICK 메뉴 취소")
def delete_pick_menu(db:Session=Depends(get_db), food_name:str=None):
    db_food = db.query(Foods).filter(Foods.name == food_name).first()
    
    if db_food is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 음식이 존재하지 않습니다.")
    
    db_food.pick = False
    db.commit()
    return {"msg":"사장의 PICK 메뉴에서 삭제되었습니다."}

