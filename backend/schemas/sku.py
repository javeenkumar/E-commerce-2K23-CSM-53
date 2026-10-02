from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class SKUBase(BaseModel):
    sku_code: str = Field(..., min_length=3, max_length=60)
    price: Decimal = Field(..., ge=0, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True, alias="active")
    option_values: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)

class SKUCreate(SKUBase):
    variant_id: Optional[int] = None

class SKUUpdate(BaseModel):
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = Field(None, alias="active")
    option_values: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(populate_by_name=True)

class SKUResponse(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int] = None
    sku_code: str
    price: Decimal
    stock_quantity: int
    is_active: bool
    option_values: Dict[str, Any] = {}
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
