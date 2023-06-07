from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from routes.orders import orders_crud, orders_schema

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)

@router.get("/list", summary="주문 목록 조회")
def get_orders_list(db: Session = Depends(get_db)):
    """
    주문 목록을 조회합니다.
    """
    cnt, orders_list = orders_crud.get_orders_list(db)

    if cnt == 0:
        return []
    else:    
        return {
            'total': cnt,
            'order_list': orders_list
        }

@router.get("/detail", summary="특정 테이블의 주문 상세 조회")
def get_orders_detail(table_id: int, db: Session = Depends(get_db)):
    """
    특정 테이블의 주문 상세를 조회합니다.
    """
    db_order_detail = orders_crud.get_order(db, table_id=table_id)
    if db_order_detail is None:
        return []
    else:
        return db_order_detail

@router.post("/create", summary="주문 생성", status_code=status.HTTP_204_NO_CONTENT)
def create_orders(order_create: orders_schema.OrdersCreate, db: Session = Depends(get_db)):
    """
    주문을 생성합니다.
    """
    orders_crud.create_order(db=db, order_create=order_create)
    return Response(status_code=status.HTTP_201_CREATED)

@router.post("/call", summary="호출하기", status_code=status.HTTP_204_NO_CONTENT)
def call_manager(call: orders_schema.Call, db: Session = Depends(get_db)):
    """
    관리자를 호출합니다.
    """
    orders_crud.call_order(db, call=call)
    return Response(status_code=status.HTTP_201_CREATED)

@router.put("/update", summary="주문 수정", status_code=status.HTTP_204_NO_CONTENT)
def update_order(order_update: orders_schema.OrdersUpdate, db: Session = Depends(get_db)):
    """
    주문을 수정합니다.
    """
    db_query = orders_crud.get_order(db, table_id=order_update.order_id)

    if db_query is None:
        raise HTTPException(status_code=404, detail="Order not found")

    orders_crud.update_order(db=db, order_update=order_update)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/delete", summary="주문 삭제", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_delete: orders_schema.OrdersDelete, db: Session = Depends(get_db)):
    """
    주문을 삭제합니다.
    """
    db_query = orders_crud.get_order(db, table_id=order_delete)

    if db_query is None:
        raise HTTPException(status_code=404, detail="Order not found")

    orders_crud.delete_order(db=db, order_delete=order_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/call/list", summary="호출 목록 조회")
def get_call_list(db: Session = Depends(get_db)):
    """
    호출 목록을 조회합니다.
    """
    call_list = orders_crud.get_call_list(db)
    return call_list
