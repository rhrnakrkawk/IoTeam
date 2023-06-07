from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models import Orders, Foods, Tables, Stocks, Receipts
from routes.orders import orders_schema
from datetime import datetime
import pytz


utc_now = datetime.now(pytz.utc)
korea_timezone = pytz.timezone('Asia/Seoul')

def get_orders_list(db: Session):
    """
    전체 주문 목록 확인

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        int: 주문의 총 개수
        list: 주문 목록
    """
    orders_list = db.query(Orders).all()
    total = db.query(Orders).count()

    return total, orders_list


def get_order(db: Session, table_id: int):
    """
    특정 테이블의 주문 상세 조회

    Args:
        db (Session): SQLAlchemy 세션 객체
        table_id (int): 조회할 테이블의 ID

    Returns:
        Orders: 주문 정보
    """
    order = db.query(Orders).filter(Orders.table_id == table_id).first()
    return order


def create_order(db: Session, order_create: orders_schema.OrdersCreate):
    """
    주문 생성

    Args:
        db (Session): SQLAlchemy 세션 객체
        order_create (OrdersCreate): 주문 생성에 필요한 정보

    Raises:
        ValueError: 주문 생성 실패 시 발생하는 예외

    Returns:
        dict: 응답 메시지
    """
    table_id = order_create.table_id
    menus = order_create.menus
    db_table = db.query(Tables).filter(
        and_(
            (Tables.table_id == table_id),
            or_((Tables.is_paid == False), (Tables.is_paid == 0)),
        )
    ).first()
    if db_table is None:
        raise ValueError("해당 테이블이 존재하지 않습니다.")

    total_price = 0

    for menu in menus:
        food_name = menu["food_name"]
        amount = menu["amount"]

        db_food = db.query(Foods).filter(Foods.name == food_name).first()
        if db_food is None:
            raise ValueError(f"해당 음식({food_name})이 존재하지 않습니다.")

        db_receipts = db.query(Receipts).filter(
            Receipts.food_name == food_name
        ).all()
        db_receipts_cnt = len(db_receipts)
        cnt = 0
        for receipt in db_receipts:
            db_stock = db.query(Stocks).filter(Stocks.name == receipt.name).first()
            if db_stock is None:
                raise ValueError(
                    f"해당 음식({food_name})의 재료({receipt.name})의 재고가 존재하지 않습니다."
                )
            cnt += 1

        if cnt != db_receipts_cnt:
            raise ValueError(
                f"해당 음식({food_name})의 재료의 개수가 일치하지 않습니다."
            )

        total_price += amount * db_food.price

        for receipt in db_receipts:
            db_stock = db.query(Stocks).filter(Stocks.name == receipt.name).first()
            db_stock.amount -= receipt.amount * amount
            db.add(db_stock)

        db_order = Orders(
            table_id=table_id,
            menu=food_name,
            amount=amount,
            order_time=datetime.now(pytz.utc).astimezone(korea_timezone).strftime(
                "%Y-%m-%d"
            ),
        )
        db.add(db_order)

        db_food = db.query(Foods).filter(Foods.name == food_name).first()
        db_food.populate += amount
        db.add(db_food)

    db_table.total_price += total_price
    db.add(db_table)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    return {"message": "주문이 성공적으로 생성되었습니다."}


def call_order(db: Session, call: orders_schema.Call):
    """
    주문 호출 생성

    Args:
        db (Session): SQLAlchemy 세션 객체
        call (Call): 주문 호출 정보

    Raises:
        ValueError: 주문 호출 생성 실패 시 발생하는 예외

    Returns:
        dict: 응답 메시지
    """
    db_table = db.query(Tables).filter(Tables.table_id == call.table_id).first()
    if db_table is None:
        raise ValueError("해당 테이블이 존재하지 않습니다.")
    db_order = Orders(
        table_id=call.table_id, call=call.call, content=call.content
    )
    db.add(db_order)
    db.commit()
    return {"message": "호출 완료"}


def update_order(db: Session, order_update: orders_schema.OrdersUpdate):
    """
    주문 정보 업데이트

    Args:
        db (Session): SQLAlchemy 세션 객체
        order_update (OrdersUpdate): 주문 업데이트 정보

    Raises:
        ValueError: 주문 업데이트 실패 시 발생하는 예외
    """
    db_order = db.query(Orders).filter(
        Orders.table_id == order_update.order_id
    ).first()
    if db_order is None:
        raise ValueError("해당 주문이 존재하지 않습니다.")

    db_order.menu = order_update.menu
    db_order.amount = order_update.amount
    db.add(db_order)
    db.commit()


def delete_order(db: Session, id: orders_schema.OrdersDelete):
    """
    주문 삭제

    Args:
        db (Session): SQLAlchemy 세션 객체
        id (OrdersDelete): 주문 삭제 정보
    """
    db_order = db.query(Orders).filter(Orders.table_id == id)
    db.delete(db_order)
    db.commit()


def call_list(db: Session):
    """
    호출된 주문 목록 확인

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        list: 호출된 주문 목록
    """
    db_call = db.query(Orders).filter(Orders.call == True).all()
    return db_call
