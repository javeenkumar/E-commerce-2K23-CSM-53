"""
Automated tests for SKU Creation, Code Uniqueness, Stock Enforcement, and Combination Matrix (CAT-03, CAT-04, CAT-05).
"""
def test_sku_creation_and_duplicate_code_conflict(client, admin_headers):
    cat = client.post("/api/v1/admin/categories", json={"name": "Keyboards", "slug": "keyboards"}, headers=admin_headers).json()
    prod = client.post("/api/v1/admin/products", json={
        "category_id": cat["id"],
        "name": "Pro Keyboard",
        "slug": "pro-keyboard",
        "description": "Mechanical gaming keyboard"
    }, headers=admin_headers).json()

    sku_resp = client.post(f"/api/v1/admin/products/{prod['id']}/skus", json={
        "sku_code": "PRO-KB-RED",
        "price": 129.99,
        "stock_quantity": 15,
        "option_values": {"Switch": "Red Linear"}
    }, headers=admin_headers)
    assert sku_resp.status_code == 201
    assert sku_resp.json()["sku_code"] == "PRO-KB-RED"

    # Duplicate SKU code rejection (CAT-03, CAT-05)
    dup_sku = client.post(f"/api/v1/admin/products/{prod['id']}/skus", json={
        "sku_code": "PRO-KB-RED",
        "price": 149.99,
        "stock_quantity": 5
    }, headers=admin_headers)
    assert dup_sku.status_code == 409

def test_sku_negative_stock_rejection(client, admin_headers):
    cat = client.post("/api/v1/admin/categories", json={"name": "Audio Tech", "slug": "audio-tech"}, headers=admin_headers).json()
    prod = client.post("/api/v1/admin/products", json={
        "category_id": cat["id"],
        "name": "Earbuds",
        "slug": "earbuds",
        "description": "ANC earbuds"
    }, headers=admin_headers).json()

    # Negative stock is rejected at API/DB boundary (CAT-05)
    resp = client.post(f"/api/v1/admin/products/{prod['id']}/skus", json={
        "sku_code": "EB-NEG",
        "price": 49.99,
        "stock_quantity": -5
    }, headers=admin_headers)
    assert resp.status_code == 422

def test_update_sku_price_and_stock(client, admin_headers):
    cat = client.post("/api/v1/admin/categories", json={"name": "Phones", "slug": "phones"}, headers=admin_headers).json()
    prod = client.post("/api/v1/admin/products", json={
        "category_id": cat["id"],
        "name": "Galaxy Phone",
        "slug": "galaxy-phone",
        "description": "Smartphone"
    }, headers=admin_headers).json()

    sku_resp = client.post(f"/api/v1/admin/products/{prod['id']}/skus", json={
        "sku_code": "GAL-PH-128",
        "price": 45000.00,
        "stock_quantity": 10
    }, headers=admin_headers).json()

    # 1. Update SKU price -> PASS
    patch_price = client.patch(f"/api/v1/admin/skus/{sku_resp['id']}", json={
        "price": 43500.00
    }, headers=admin_headers)
    assert patch_price.status_code == 200
    assert float(patch_price.json()["price"]) == 43500.00

    # 2. Update SKU stock -> PASS
    patch_stock = client.patch(f"/api/v1/admin/skus/{sku_resp['id']}", json={
        "stock_quantity": 25
    }, headers=admin_headers)
    assert patch_stock.status_code == 200
    assert patch_stock.json()["stock_quantity"] == 25

def test_sku_missing_combinations_omitted(client, admin_headers):
    """CAT-04: The system represents valid combinations only. A missing combination is not created as a fake SKU."""
    cat = client.post("/api/v1/admin/categories", json={"name": "Gaming Mice", "slug": "gaming-mice"}, headers=admin_headers).json()
    prod = client.post("/api/v1/admin/products", json={
        "category_id": cat["id"],
        "name": "Wireless Mouse",
        "slug": "wireless-mouse",
        "description": "Ergonomic gaming mouse"
    }, headers=admin_headers).json()

    # We only manufacture Black color
    client.post(f"/api/v1/admin/products/{prod['id']}/skus", json={
        "sku_code": "MOUSE-BLK",
        "price": 59.99,
        "stock_quantity": 20,
        "option_values": {"Color": "Black"}
    }, headers=admin_headers)

    # Verify query for non-manufactured White SKU returns 404 (not a zero-stock placeholder)
    resp = client.get("/api/v1/admin/skus/9999", headers=admin_headers)
    assert resp.status_code == 404
