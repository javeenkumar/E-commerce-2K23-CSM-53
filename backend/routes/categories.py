from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.auth import get_current_admin
from backend.models.category import Category
from backend.schemas import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryTreeNode

router = APIRouter(prefix="/categories", tags=["Categories"])

def check_category_cycle(db: Session, category_id: int, new_parent_id: Optional[int]):
    """Prevents circular dependency: a category cannot become its own ancestor (CAT-01)."""
    if new_parent_id is None:
        return
    if category_id == new_parent_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Circular dependency detected: Category cannot be its own parent."
        )
    curr_id = new_parent_id
    visited = {category_id}
    while curr_id is not None:
        if curr_id in visited:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Circular dependency detected: Category {category_id} is an ancestor of proposed parent {new_parent_id}."
            )
        visited.add(curr_id)
        parent = db.query(Category).filter(Category.id == curr_id).first()
        curr_id = parent.parent_id if parent else None

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    if payload.parent_id:
        parent = db.query(Category).filter(Category.id == payload.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail=f"Parent category {payload.parent_id} not found")

    existing = db.query(Category).filter(Category.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Category with slug '{payload.slug}' already exists")

    cat = Category(**payload.model_dump())
    db.add(cat)
    try:
        db.commit()
        db.refresh(cat)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Integrity error: Duplicate slug or invalid parent")
    return cat

@router.get("", response_model=List[CategoryTreeNode])
def get_category_tree(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    all_cats = db.query(Category).all()
    node_map = {}
    for c in all_cats:
        node_map[c.id] = CategoryTreeNode(
            id=c.id,
            name=c.name,
            slug=c.slug,
            parent_id=c.parent_id,
            description=c.description,
            is_active=c.is_active,
            created_at=c.created_at,
            children=[]
        )
    tree = []
    for c in all_cats:
        if c.parent_id and c.parent_id in node_map:
            node_map[c.parent_id].children.append(node_map[c.id])
        else:
            tree.append(node_map[c.id])
    return tree

@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "parent_id" in update_data and update_data["parent_id"] is not None:
        check_category_cycle(db, category_id, update_data["parent_id"])

    if "slug" in update_data and update_data["slug"] != cat.slug:
        existing = db.query(Category).filter(Category.slug == update_data["slug"]).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Category with slug '{update_data['slug']}' already exists")

    for k, v in update_data.items():
        setattr(cat, k, v)

    db.commit()
    db.refresh(cat)
    return cat
