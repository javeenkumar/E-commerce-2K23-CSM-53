from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class VariantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)

class VariantCreate(VariantBase):
    product_id: int

class VariantResponse(VariantBase):
    id: int
    product_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
