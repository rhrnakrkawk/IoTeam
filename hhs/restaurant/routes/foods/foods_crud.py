from routes.foods import foods_schema
from models import Foods
from sqlalchemy.orm import Session

def get_food_list(db: Session):
    """
    모든 음식 정보 출력

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        int: 음식의 총 개수
        list: 음식 목록
    """
    food_list = db.query(Foods).all()
    count = db.query(Foods).count()
    return count, food_list


def get_food(db: Session, food_id: int = 0, food_name: str = ""):
    """
    특정 음식에 대한 상세 정보 출력

    Args:
        db (Session): SQLAlchemy 세션 객체
        food_id (int, optional): 조회할 음식의 ID. Defaults to 0.
        food_name (str, optional): 조회할 음식의 이름. Defaults to "".

    Returns:
        Foods: 음식 정보
    """
    if food_id == 0:
        return db.query(Foods).filter(Foods.name == food_name).first()
    elif food_name == "":
        return db.query(Foods).filter(Foods.id == food_id).first()


def create_food(food_create: foods_schema.FoodCreate, db: Session):
    """
    새로운 음식/식재료 추가

    Args:
        food_create (FoodCreate): 음식 생성에 필요한 정보
        db (Session): SQLAlchemy 세션 객체
    """
    if db.query(Foods).filter(Foods.name == food_create.name).first():
        raise ValueError("이미 존재하는 음식입니다.")
    
    db_food = Foods(
        name=food_create.name,
        price=food_create.price,
        pick=food_create.pick,
        populate=0,
    )
    db.add(db_food)
    db.commit()


def update_food(db: Session, food_update: foods_schema.FoodUpdate):
    """
    음식 정보 수정

    Args:
        db (Session): SQLAlchemy 세션 객체
        food_update (FoodUpdate): 음식 수정에 필요한 정보
    """
    db_food = db.query(Foods).get(food_update.food_id).first()
    db_food.name = food_update.name
    db_food.price = food_update.price
    db.add(db_food)
    db.commit()


def delete_food(db: Session, food_name: str):
    """
    음식 정보 삭제

    Args:
        db (Session): SQLAlchemy 세션 객체
        food_name (str): 삭제할 음식의 이름
    """
    db_food = db.query(Foods).filter(Foods.name == food_name).first()
    db.delete(db_food)
    db.commit()
