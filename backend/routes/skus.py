from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.auth import get_current_admin
from backend.models.sku import SKU
from backend.schemas import SKUUpdate, SKUResponse

router = APIRouter(prefix="/skus", tags=["SKUs"])

@router.patch("/{sku_id}", response_model=SKUResponse)
def update_sku(
    sku_id: int,
    payload: SKUUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    sku = db.query(SKU).filter(SKU.id == sku_id).first()
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(sku, k, v)

    try:
        db.commit()
        db.refresh(sku)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint violation on SKU update")
    return sku

@router.get("/{sku_id}", response_model=SKUResponse)
def get_sku(
    sku_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    sku = db.query(SKU).filter(SKU.id == sku_id).first()
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    return sku
