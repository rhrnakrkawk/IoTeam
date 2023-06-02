from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
class Orders(BaseModel):
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
    
    table_id:int
    menus:List[dict]

    @validator('menus')
    def quantity_must_be_positive(cls, value):
        if not value:
            raise ValueError('입력이 없습니다.')
        return value

class OrdersList(BaseModel):
    total:int
    order_list:List[Orders]=[]
    
class OrdersUpdate(OrdersCreate):
    order_id:int
    
class OrdersDelete(BaseModel):
    order_id:int