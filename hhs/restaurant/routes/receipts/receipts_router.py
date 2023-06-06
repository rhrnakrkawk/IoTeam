from fastapi import APIRouter, Depends,Response
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from routes.receipts import receipts_schema, receipts_crud

router = APIRouter(
    prefix="/api/receipts",
    tags=["Receipts"]
)

@router.get("/list", response_model=receipts_schema.ReceiptsList,summary="레시피 목록 전체 조회")
def receipts_list(db: Session = Depends(get_db)):
    total,_receipts_list = receipts_crud.get_receipts_list(db)
    print(total,_receipts_list)
    if total == 0:
        return {
            "total":total,
            "receipts_list":"없음."
        }
    else:
        return {
            "total":total,
            "Receipts_list":_receipts_list
        }
    
@router.get("/detail/{receipts_name}",response_model=receipts_schema.ReceiptsDetail,summary="특정 레시피 상세 조회")
def receipts_detail(receipts_name: str, db: Session = Depends(get_db)):
    receipts = receipts_crud.get_receipts(db, receipts_name=receipts_name)
    ret_receipts = {
        "food_name":receipts[0].food_name,
        "content":{}
    }

    for receipt in receipts:
        ret_receipts["content"][receipt.name] = receipt.amount
        
    return ret_receipts

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT,summary="레시피 추가")
def receipts_create(_receipts_create: receipts_schema.ReceiptsCreate,
                    db: Session = Depends(get_db)):
    receipts_crud.create_receipts(db=db, receipts_create=_receipts_create)
    return Response(status_code=status.HTTP_201_CREATED)
    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT,summary="레시피 삭제")
def receipts_delete(_receipts_delete:int,
                    db: Session = Depends(get_db)):
    receipts_crud.delete_receipts(db=db, receipts_id=_receipts_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)