from pydantic import BaseModel, validator
from typing import List

class Food(BaseModel):
    name: str
    price: int
    
    class Config:
        orm_mode = True
        
class FoodCreate(BaseModel):
    name: str
    price: int
    # 소모 재료
    # 재료 이름 : 재료 소모량
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('가격은 0보다 커야 합니다.')
        return v

class FoodList(BaseModel):
    total: int = 0
    food_list: List[Food] = []
    
class FoodUpdate(FoodCreate):
    food_id: int

class FoodDelete(BaseModel):
    food_id: int
