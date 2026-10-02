from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from backend.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sku_id = Column(Integer, ForeignKey("skus.id", ondelete="SET NULL"), nullable=True)
    url = Column(String(500), nullable=False)
    role = Column(String(30), default="GALLERY", nullable=False)
    alt_text = Column(String(200), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('THUMBNAIL', 'GALLERY', 'BANNER')", name="chk_asset_role"),
    )

    product = relationship("Product", back_populates="assets")
    sku = relationship("SKU", back_populates="assets")
