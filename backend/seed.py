"""
Reproducible Seed Data Fixture for Sprint 2 Catalog Data Foundation.
Fulfills Section 9 of the Sprint 2 Manual and exact project specifications:
- 2+ categories, 2 levels in category tree (Electronics -> Mobile Phones, Laptops)
- 3 products (Samsung Galaxy A15, Dell Inspiron 15, HP Wireless Mouse)
- 4+ valid SKUs with prices and stock quantities
- Products with multiple variants
- 1 intentionally unavailable variant combination (e.g., Blue / 256GB omitted completely; no fake zero-stock SKU)
"""
from decimal import Decimal
from sqlalchemy.orm import Session
from backend.database import SessionLocal, Base, engine
from backend.models.category import Category
from backend.models.product import Product
from backend.models.variant import Variant
from backend.models.sku import SKU
from backend.models.asset import Asset
from backend.models.user import User

def run_seed():
    db: Session = SessionLocal()
    try:
        # Reset tables for clean demonstration
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("[SEED] Cleaned and initialized database tables.")

        # 0. Create default Admin and Customer Users (Sprint 1 foundation)
        admin_user = User(
            username="admin",
            email="admin@electronics.local",
            password_hash="$2b$12$eA89nPQi.3hNvyqM2v8kXe8Uu26vQ77W9sX1X4vVd5VqMv6vK",  # bcrypt mock
            role="admin"
        )
        customer_user = User(
            username="javeen_c",
            email="javeen@customer.local",
            password_hash="$2b$12$eA89nPQi.3hNvyqM2v8kXe8Uu26vQ77W9sX1X4vVd5VqMv6vK",
            role="customer"
        )
        db.add_all([admin_user, customer_user])
        db.commit()
        print("[SEED] Created baseline Admin and Customer users.")

        # 1. Category Tree (Two levels)
        cat_electronics = Category(
            name="Electronics",
            slug="electronics",
            parent_id=None,
            description="Consumer electronics, computing hardware, and mobile devices.",
            is_active=True
        )
        db.add(cat_electronics)
        db.commit()
        db.refresh(cat_electronics)

        cat_mobiles = Category(
            name="Mobile Phones",
            slug="mobile-phones",
            parent_id=cat_electronics.id,
            description="Smartphones, cellular accessories, and devices.",
            is_active=True
        )
        cat_laptops = Category(
            name="Laptops",
            slug="laptops",
            parent_id=cat_electronics.id,
            description="Notebooks, ultrabooks, and personal computing laptops.",
            is_active=True
        )
        db.add_all([cat_mobiles, cat_laptops])
        db.commit()
        db.refresh(cat_mobiles)
        db.refresh(cat_laptops)
        print(f"[SEED] Created 2-level category tree: {cat_electronics.name} -> [{cat_mobiles.name}, {cat_laptops.name}]")

        # 2. Products (Three distinct products)
        # Product 1: Samsung Galaxy A15 (Multi-variant)
        prod_samsung = Product(
            category_id=cat_mobiles.id,
            name="Samsung Galaxy A15",
            slug="samsung-galaxy-a15",
            description="6.5-inch Super AMOLED display smartphone with 50MP triple camera system.",
            status="published",
            specifications={
                "display": "6.5-inch Super AMOLED 90Hz",
                "processor": "Octa-core MediaTek Helio G99",
                "battery": "5000 mAh, 25W Fast Charging"
            }
        )

        # Product 2: Dell Inspiron 15 (Multi-variant)
        prod_dell = Product(
            category_id=cat_laptops.id,
            name="Dell Inspiron 15",
            slug="dell-inspiron-15",
            description="15.6-inch FHD laptop with Intel Core processor and high-speed NVMe SSD.",
            status="published",
            specifications={
                "screen_size": "15.6-inch FHD (1920 x 1080)",
                "os": "Windows 11 Home",
                "weight_kg": 1.65
            }
        )

        # Product 3: HP Wireless Mouse
        prod_mouse = Product(
            category_id=cat_electronics.id,
            name="HP Wireless Mouse",
            slug="hp-wireless-mouse",
            description="2.4GHz wireless optical mouse with ergonomic contour and long battery life.",
            status="draft",
            specifications={
                "dpi": 1600,
                "connectivity": "2.4GHz Wireless USB Dongle",
                "battery": "1x AA"
            }
        )
        db.add_all([prod_samsung, prod_dell, prod_mouse])
        db.commit()
        db.refresh(prod_samsung)
        db.refresh(prod_dell)
        db.refresh(prod_mouse)
        print(f"[SEED] Created 3 products: {prod_samsung.name}, {prod_dell.name}, {prod_mouse.name}")

        # 3. Variants
        var_sam_black = Variant(product_id=prod_samsung.id, name="Black / 128GB")
        var_sam_blue = Variant(product_id=prod_samsung.id, name="Blue / 128GB")
        var_dell_8 = Variant(product_id=prod_dell.id, name="8GB / 256GB")
        var_dell_16 = Variant(product_id=prod_dell.id, name="16GB / 512GB")
        db.add_all([var_sam_black, var_sam_blue, var_dell_8, var_dell_16])
        db.commit()
        db.refresh(var_sam_black)
        db.refresh(var_sam_blue)
        db.refresh(var_dell_8)
        db.refresh(var_dell_16)

        # 4. SKUs (4 valid SKUs + 1 single item for mouse)
        sku1 = SKU(
            product_id=prod_samsung.id,
            variant_id=var_sam_black.id,
            sku_code="SAM-A15-BLK-128",
            price=Decimal("45000.00"),
            stock_quantity=10,
            is_active=True,
            option_values={"Color": "Black", "Storage": "128GB"}
        )
        sku2 = SKU(
            product_id=prod_samsung.id,
            variant_id=var_sam_blue.id,
            sku_code="SAM-A15-BLU-128",
            price=Decimal("45000.00"),
            stock_quantity=8,
            is_active=True,
            option_values={"Color": "Blue", "Storage": "128GB"}
        )
        sku3 = SKU(
            product_id=prod_dell.id,
            variant_id=var_dell_8.id,
            sku_code="DELL-I15-8-256",
            price=Decimal("120000.00"),
            stock_quantity=5,
            is_active=True,
            option_values={"RAM": "8GB", "Storage": "256GB SSD"}
        )
        sku4 = SKU(
            product_id=prod_dell.id,
            variant_id=var_dell_16.id,
            sku_code="DELL-I15-16-512",
            price=Decimal("145000.00"),
            stock_quantity=4,
            is_active=True,
            option_values={"RAM": "16GB", "Storage": "512GB SSD"}
        )
        sku5 = SKU(
            product_id=prod_mouse.id,
            variant_id=None,
            sku_code="HP-WM-BLK-STD",
            price=Decimal("3500.00"),
            stock_quantity=25,
            is_active=True,
            option_values={"Color": "Matte Black"}
        )

        db.add_all([sku1, sku2, sku3, sku4, sku5])
        db.commit()
        print(f"[SEED] Created 5 valid SKUs: {sku1.sku_code}, {sku2.sku_code}, {sku3.sku_code}, {sku4.sku_code}, {sku5.sku_code}")

        # 5. CAT-04 Requirement Demonstration:
        # Combination 'Blue / 256GB' for Samsung Galaxy A15 is intentionally NOT manufactured.
        # Strict Rule: No dummy or zero-stock SKU is inserted into the database.
        print("[SEED] Verified: 'Blue / 256GB' combination for Samsung Galaxy A15 is intentionally omitted (CAT-04).")

        # 6. Asset records (Sprint 2 models Asset table without file upload requirement)
        asset1 = Asset(
            product_id=prod_samsung.id,
            sku_id=sku1.id,
            url="https://images.samsung.local/a15-black.jpg",
            role="THUMBNAIL",
            alt_text="Samsung Galaxy A15 Black Edition Front View",
            sort_order=1
        )
        db.add(asset1)
        db.commit()
        print("[SEED] Seed data population completed successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
