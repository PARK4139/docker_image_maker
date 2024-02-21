from fastapi import APIRouter
from fastapi import HTTPException, Depends
from requests import Session

from pkg_park4139_for_linux import MySqlUtil, ItemsUtil, ItemsUtil


router = APIRouter()


@router.post("/items/")
async def create_item(item: ItemsUtil.ItemCreate, db: Session = Depends(MySqlUtil.get_session)):
    db_item = ItemsUtil.create_item(db, item)
    return db_item


@router.get("/items/")
async def get_items(db: Session = Depends(MySqlUtil.get_session)):
    items = ItemsUtil.get_items(db)
    return items


@router.get("/items/{id}")
async def get_item(id: int, db: Session = Depends(MySqlUtil.get_session)):
    item = ItemsUtil.get_item(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없었습니다")
    return item


@router.put("/items/{id}")
async def update_item(id: int, updated_item: ItemsUtil.ItemCreate, db: Session = Depends(MySqlUtil.get_session)):
    db_item = ItemsUtil.get_item(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없었습니다")
    updated_item = ItemsUtil.update_item(db, db_item, updated_item)
    return updated_item


@router.delete("/items/{id}")
async def delete_item(id: int, db: Session = Depends(MySqlUtil.get_session)):
    db_item = ItemsUtil.get_item(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없었습니다")
    ItemsUtil.delete_item(db, db_item)
    return {"message": "Item deleted successfully"}
