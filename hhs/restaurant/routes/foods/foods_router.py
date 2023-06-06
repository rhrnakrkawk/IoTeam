from fastapi import APIRouter, Depends,HTTPException,Response
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from routes.foods import foods_crud, foods_schema

router = APIRouter(
    prefix="/api/food",
    tags=["Food"]
)

@router.get("/list", response_model=foods_schema.FoodList,summary="음식 목록 전체 조회")
def get_food_list(db: Session = Depends(get_db)):
    cnt, db_result = foods_crud.get_food_list(db)
    if cnt ==0:
        return []
    else:
        return {
            'total': cnt,
            'food_list': db_result
        }

@router.get("/detail/{food_name}", response_model=foods_schema.Food,summary="특정 음식 상세 조회(이름으로 호출)")
def get_food(food_name:str,db:Session=Depends(get_db)):
    
    db_result = foods_crud.get_food(db,food_name=food_name)
    if  db_result is None:
        return []
    else:
        return db_result

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT,summary="음식 추가")
def create_food(food_create: foods_schema.FoodCreate,db: Session = Depends(get_db)):
    foods_crud.create_food(db=db, food_create=food_create)
    return Response(status_code=status.HTTP_201_CREATED)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT,summary="음식 수정")
def update_food(food_update: foods_schema.FoodUpdate, db: Session = Depends(get_db)):
    db_food = foods_crud.get_food(db, food_id=food_update)
    
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    foods_crud.update_food(db=db, food_update=food_update)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT,summary="음식 삭제")
def delete_food(food_name: str, db: Session = Depends(get_db)):
    db_food = foods_crud.get_food(db, food_name=food_name)
    
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    foods_crud.delete_food(db, food_name=food_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)