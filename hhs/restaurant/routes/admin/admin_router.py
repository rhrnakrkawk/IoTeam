from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from routes.foods import foods_router
from routes.receipts import receipts_router
from routes.orders import orders_router
from routes.stocks import stocks_router
from routes.tables import tables_router

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.get("/populate")
def get_populate_food(db:Session=Depends(get_db)):
    