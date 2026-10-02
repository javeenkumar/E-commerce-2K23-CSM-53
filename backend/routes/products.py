from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.auth import get_current_admin
from backend.models.product import Product
from backend.models.category import Category
from backend.models.variant import Variant
from backend.models.sku import SKU
from backend.schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    VariantCreate, VariantResponse,
    SKUCreate, SKUResponse
)

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    cat = db.query(Category).filter(Category.id == payload.category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail=f"Category {payload.category_id} not found")

    existing = db.query(Product).filter(Product.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product with slug '{payload.slug}' already exists")

    product = Product(**payload.model_dump())
    db.add(product)
    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database integrity violation")
    return product

@router.get("")
def list_admin_products(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    offset = (page - 1) * limit
    products = db.query(Product).offset(offset).limit(limit).all()
    total = db.query(Product).count()
    items = []
    for p in products:
        items.append({
            "id": p.id,
            "category_id": p.category_id,
            "category_name": p.category.name if p.category else None,
            "name": p.name,
            "slug": p.slug,
            "status": p.status,
            "sku_count": len(p.skus),
            "created_at": p.created_at
        })
    return {"total": total, "page": page, "limit": limit, "items": items}

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "category_id" in update_data and update_data["category_id"] is not None:
        cat = db.query(Category).filter(Category.id == update_data["category_id"]).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Target category not found")

    if "slug" in update_data and update_data["slug"] != product.slug:
        existing = db.query(Product).filter(Product.slug == update_data["slug"]).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Product with slug '{update_data['slug']}' already exists")

    for k, v in update_data.items():
        setattr(product, k, v)

    db.commit()
    db.refresh(product)
    return product

@router.post("/{product_id}/variants", response_model=VariantResponse, status_code=status.HTTP_201_CREATED)
def create_product_variant(
    product_id: int,
    name: str,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    variant = Variant(product_id=product_id, name=name)
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant

@router.post("/{product_id}/skus", response_model=SKUResponse, status_code=status.HTTP_201_CREATED)
def create_product_sku(
    product_id: int,
    payload: SKUCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    if payload.variant_id:
        var = db.query(Variant).filter(Variant.id == payload.variant_id, Variant.product_id == product_id).first()
        if not var:
            raise HTTPException(status_code=404, detail=f"Variant {payload.variant_id} not found under this product")

    existing_sku = db.query(SKU).filter(SKU.sku_code == payload.sku_code.upper()).first()
    if existing_sku:
        raise HTTPException(status_code=409, detail=f"SKU code '{payload.sku_code}' already exists")

    sku_dict = payload.model_dump()
    sku_dict["sku_code"] = sku_dict["sku_code"].upper()
    sku = SKU(product_id=product_id, **sku_dict)
    db.add(sku)
    try:
        db.commit()
        db.refresh(sku)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Database constraint violation on SKU creation")
    return sku
