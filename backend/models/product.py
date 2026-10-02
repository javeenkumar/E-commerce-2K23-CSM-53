from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from backend.database import Base, FlexibleJSON

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    status = Column(String(20), default="draft", nullable=False)
    specifications = Column(FlexibleJSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("LOWER(status) IN ('draft', 'published', 'archived', 'inactive')", name="chk_product_status"),
    )

    category = relationship("Category", back_populates="products")
    variants = relationship("Variant", back_populates="product", cascade="all, delete-orphan")
    skus = relationship("SKU", back_populates="product", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="product", cascade="all, delete-orphan")
