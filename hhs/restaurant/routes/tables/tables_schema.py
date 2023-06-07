from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
class Table(BaseModel):
    id:int
    table_id : int
    customer_count:int
    total_price:int=0
    table_time:datetime=None
    is_paid:bool=False
    class Config:
        orm_mode = True
        
class TableCreate(BaseModel):
    table_id:int
    customer_count:int
    
    @validator('customer_count')
    def not_empty(cls, v):
        if not v:
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
class TableList(BaseModel):
    total:int = 0
    table_list : List[Table] = []
    
class TableUpdate(TableCreate):
    table_id :int

class TableDelete(BaseModel):
    table_id:int
