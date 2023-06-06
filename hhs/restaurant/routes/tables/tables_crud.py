from routes.tables import tables_schema
from models import Tables
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
import pytz

utc_now = datetime.now(pytz.utc)
korea_timezone = pytz.timezone('Asia/Seoul')

def get_table_list(db: Session):
    """
    테이블 목록 조회

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        int: 테이블의 총 개수
        list: 테이블 목록
    """
    table_list = db.query(Tables).all()
    total = len(table_list)
    return total, table_list


def get_table(db: Session, table_id: int):
    """
    특정 테이블 조회

    Args:
        db (Session): SQLAlchemy 세션 객체
        table_id (int): 조회할 테이블의 ID

    Returns:
        Tables: 조회된 테이블 객체
    """
    table = db.query(Tables).filter(Tables.table_id == table_id).first()
    return table


def create_table(db: Session, table_create: tables_schema.TableCreate):
    """
    새로운 테이블 생성

    Args:
        db (Session): SQLAlchemy 세션 객체
        table_create (TableCreate): 테이블 생성에 필요한 정보
    """
    db_table = Tables(
        table_id=table_create.table_id,
        customer_count=table_create.customer_count,
        total_price=table_create.total_price,
        table_time=datetime.now(pytz.utc).astimezone(korea_timezone).strftime("%Y-%m-%d")
    )
    db.add(db_table)
    db.commit()


def update_table(db: Session, table_id: int, table_update: tables_schema.TableUpdate):
    """
    테이블 정보 수정

    Args:
        db (Session): SQLAlchemy 세션 객체
        table_id (int): 수정할 테이블의 ID
        table_update (TableUpdate): 수정할 테이블 정보
    """
    db_table = db.query(Tables).filter(Tables.table_id == table_id).first()

    db_table.table_id = table_update.table_id
    db_table.customer_count = table_update.customer_count
    db_table.total_price = table_update.total_price
    db.add(db_table)
    db.commit()


def delete_table(db: Session, table_id: int):
    """
    테이블 삭제

    Args:
        db (Session): SQLAlchemy 세션 객체
        table_id (int): 삭제할 테이블의 ID
    """
    db_table = db.query(Tables).filter(Tables.table_id == table_id)
    db.delete(db_table)
    db.commit()


def pay_table(db: Session, table_id: int):
    """
    테이블 결제

    Args:
        db (Session): SQLAlchemy 세션 객체
        table_id (int): 결제할 테이블의 ID

    Raises:
        Exception: 이미 결제된 테이블인 경우 예외 발생
    """
    db_table = db.query(Tables).filter(Tables.table_id == table_id).first()
    if db_table.is_paid == False or db_table.is_paid == 0:
        db_table.is_paid = True
        db.add(db_table)
        db.commit()
    else:
        raise Exception("이미 결제된 테이블입니다.")
