from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from models import Stocks
from routes.stocks import stocks_schema, stocks_crud


router = APIRouter(
    prefix="/api/stocks",
    tags=["Stocks"]
)

@router.get("/list",response_model = stocks_schema.StocksList,summary="재고 목록 전체 조회")
def get_stocks_list(db:Session = Depends(get_db)):
    
    total,_stock_list = stocks_crud.get_stocks_list(db)
    if total == 0:
        return []
    else:
        return {
            "total":total,
            "stocks_list":_stock_list
        }
        
@router.get("/detail/{stock_id}",response_model = stocks_schema.Stocks,summary="특정 재고 상세 조회")
def get_stock(stock_id:int,db:Session = Depends(get_db)):
    stock = stocks_crud.get_stock(db,stock_id=stock_id)
    return stock

@router.post("/create",status_code=status.HTTP_204_NO_CONTENT,summary="재고 추가")
def create_stocks(_stock_create:stocks_schema.StocksCreate,
                  db:Session = Depends(get_db)):
    stocks_crud.create_stocks(db=db,stock_create=_stock_create)
    
@router.put("/update",status_code=status.HTTP_204_NO_CONTENT,summary="재고 수정")
def update_stocks(_stock_update:stocks_schema.StocksUpdate,db:Session = Depends(get_db)):
        
    db_stock = stocks_crud.get_stock(db,stock_id=_stock_update.stock_id)
    # 해당 번호의 재료가 없을 시, 400 에러를 반환
    if not db_stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    
    stocks_crud.update_stocks(db=db,prev_stock=db_stock,stock_update=_stock_update)

@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT,summary="재고 삭제")
def delete_stocks(_stock_delete:stocks_schema.StocksDelete,db:Session=Depends(get_db)):
    
    db_stock = db.query(Stocks).get(_stock_delete)
    print(db_stock.name)
    if not db_stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    
    stocks_crud.delete_stocks(db,db_stock)
    