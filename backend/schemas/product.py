from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    category_id: int
    name: str = Field(..., min_length=2, max_length=200)
    slug: str = Field(..., min_length=2, max_length=220, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str
    status: str = Field(default="draft", pattern=r"^(draft|published|archived|DRAFT|PUBLISHED|ARCHIVED)$")
    specifications: Dict[str, Any] = Field(default_factory=dict)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern=r"^(draft|published|archived|DRAFT|PUBLISHED|ARCHIVED)$")
    specifications: Optional[Dict[str, Any]] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
