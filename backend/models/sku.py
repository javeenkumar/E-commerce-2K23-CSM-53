from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from backend.database import Base, FlexibleJSON

class SKU(Base):
    __tablename__ = "skus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    variant_id = Column(Integer, ForeignKey("variants.id", ondelete="SET NULL"), nullable=True)
    sku_code = Column(String(60), nullable=False, unique=True, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    option_values = Column(FlexibleJSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("price >= 0.00", name="chk_sku_price_non_negative"),
        CheckConstraint("stock_quantity >= 0", name="chk_sku_stock_non_negative"),
    )

    product = relationship("Product", back_populates="skus")
    variant = relationship("Variant", back_populates="skus")
    assets = relationship("Asset", back_populates="sku")
