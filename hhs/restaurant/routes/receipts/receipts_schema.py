from pydantic import BaseModel, validator
from typing import List
class Receipts(BaseModel):
    food_name: str
    name: str
    amount: int
    class Config:
        orm_mode = True
        

class ReceiptsCreate(BaseModel):
    food_name:str
    content:dict
    
    @validator('food_name','content')
    def not_empty(cls, v):
        if not v:
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
        
    
class ReceiptsList(BaseModel):
    total:int = 0
    Receipts_list : List[Receipts] = []

class ReceiptsDetail(BaseModel):
    food_name: str
    content:dict

class ReceiptsUpdate(ReceiptsCreate):
    Receipts_id: int
    
    class Config:
        orm_mode = True
        
class ReceiptsDelete(BaseModel):
    Receipts_id: int
    