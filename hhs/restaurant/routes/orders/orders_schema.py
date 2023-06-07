from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import pytz
utc_now = datetime.now(pytz.utc)
korea_timezone = pytz.timezone('Asia/Seoul')

class Orders(BaseModel):
    """
    주문 정보
    """
    id: int
    
    table_id:int
    
    menu:str
    amount:int
    
    call:bool=False
    content:str=None
    order_time:datetime
    class config:
        orm_mode = True
        

class OrdersCreate(BaseModel):
    """
    주문 생성에 필요한 정보
    table_id: 테이블 번호
    menus: 주문한 메뉴 리스트
    """
    table_id:int
    menus:List[dict]
    
    @validator('menus')
    def quantity_must_be_positive(cls, value):
        if not value:
            raise ValueError('입력이 없습니다.')
        return value

class OrdersList(BaseModel):
    """
    전체 주문 조회시 반환되는 정보 형태
    """
    total:int
    order_list:List[Orders]=[]
    
class OrdersUpdate(OrdersCreate):
    """
    주문 수정에 필요한 정보
    주문 생성 상속으로 구현
    """
    order_id:int
    
class OrdersDelete(BaseModel):
    """
    주문 삭제에 필요한 정보
    order_id: 테이블 번호
    """
    order_id:int
    
class Call(BaseModel):
    """
    관리자 호출에 필요한 정보
    """
    table_id:int
    call:bool=True
    content:str