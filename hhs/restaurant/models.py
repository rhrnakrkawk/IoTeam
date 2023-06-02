from sqlalchemy import Column, Integer, String, ForeignKey,Boolean,DateTime
from sqlalchemy.orm import relationship
from database import Base

# 음식에 대한 기본적인 테이블
class Foods(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    populate = Column(Integer, nullable=False)
    pick = Column(Boolean, nullable=False, default=False)
# 음식을 만들 때 필요한 재료의 정보 저장 테이블
class Receipts(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    food_name = Column(String(255),nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    
# 현재 가게 내에 저장된 재료의 정보 저장 테이블
class Stocks(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    

class Tables(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    # 1~9번 테이블
    table_id = Column(Integer, nullable=False)
    
    # 테이블에 앉아있는 손님 수
    customer_count = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    
    # 계산 여부 확인
    # TODO: 계산 여부 확인
    
    is_paid = Column(Boolean, nullable=False, default=False)


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    
    # 테이블 정보
    table_id = Column(Integer, nullable=False)
    
    # 메뉴 정보
    menu = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    
    # 호출
    call = Column(Boolean, nullable=False, default=False)
    content = Column(String(255), nullable=True)
    # TODO: 주문한 시간
    order_time = Column(DateTime, nullable=False)