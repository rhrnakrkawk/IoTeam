from routes.foods import foods_schema
from models import Foods
from sqlalchemy.orm import Session

def get_food_list(db: Session):
    # 모든 Food 정보 출력
    food_list = db.query(Foods).all()
    count = db.query(Foods).count()
    # return
    return count, food_list

# 해당 번호의 음식에 대한 detail 정보 출력
def get_food(db: Session,food_id:int=0,food_name:str=""):
    if food_id == 0:
        return db.query(Foods).filter(Foods.name == food_name).first()
    elif food_name == "":
        return db.query(Foods).filter(Foods.id == food_id).first()

# 새로운 음식/식재료 추가
def create_food(food_create: foods_schema.FoodCreate,
                db: Session):

    db_food = Foods(name=food_create.name,
                   price=food_create.price,
                   pick=food_create.pick,
                   populate=0
                   )
    db.add(db_food)
    db.commit()
    
# 음식 정보 수정
def update_food(db:Session, food_update: foods_schema.FoodUpdate):
    db_food = db.query(Foods).get(food_update.food_id)
    db_food.name = food_update.name
    db_food.price = food_update.price
    db.add(db_food)
    db.commit()
    
# 음식 정보 삭제
def delete_food(db:Session, food_name:str):
    db_food = db.query(Foods).get(Foods.name==food_name)
    db.delete(db_food)
    db.commit()
    
    