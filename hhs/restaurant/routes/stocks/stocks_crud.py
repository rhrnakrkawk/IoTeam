from sqlalchemy.orm import Session
from routes.stocks.stocks_schema import StocksCreate, StocksUpdate
from models import Stocks

def get_stocks_list(db: Session):
    """
    재고 전체 리스트 조회

    Args:
        db (Session): SQLAlchemy 세션 객체

    Returns:
        int: 재고의 총 개수
        list: 재고 목록
    """
    stocks_list = db.query(Stocks).all()
    total = db.query(Stocks).count()
    return total, stocks_list


def get_stock(db: Session, stock_id: int = 0, stock_name: str = ""):
    """
    재고 상세 조회

    Args:
        db (Session): SQLAlchemy 세션 객체
        stock_id (int, optional): 조회할 재고의 ID. Defaults to 0.
        stock_name (str, optional): 조회할 재고의 이름. Defaults to "".

    Returns:
        Stocks: 조회된 재고 객체
    """
    if stock_id == 0:
        return db.query(Stocks).filter(Stocks.name == stock_name).first()
    elif stock_name == "":
        return db.query(Stocks).get(stock_id).first()


def create_stocks(db: Session, stock_create: StocksCreate):
    """
    새로운 재고 추가

    Args:
        db (Session): SQLAlchemy 세션 객체
        stock_create (StocksCreate): 재고 생성에 필요한 정보
    """
    
    if db.query(Stocks).filter(Stocks.name == stock_create.name).first():
        raise ValueError("이미 존재하는 재고입니다.")
    
    db_stock = Stocks(name=stock_create.name, price=stock_create.price, amount=stock_create.amount)
    db.add(db_stock)
    db.commit()


def update_stocks(db: Session, prev_stock: Stocks, stock_update: StocksUpdate):
    """
    재고 정보 수정

    Args:
        db (Session): SQLAlchemy 세션 객체
        prev_stock (Stocks): 수정할 재고 객체
        stock_update (StocksUpdate): 수정할 재고 정보
    """
    prev_stock.name = stock_update.name
    prev_stock.price = stock_update.price
    prev_stock.amount = stock_update.amount

    db.add(prev_stock)
    db.commit()


def delete_stocks(db: Session, stock: Stocks):
    """
    재고 삭제

    Args:
        db (Session): SQLAlchemy 세션 객체
        stock (Stocks): 삭제할 재고 객체
    """
    db.delete(stock)
    db.commit()
