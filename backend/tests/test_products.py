"""
Automated tests for Product Identity, Slug Uniqueness, and Status Lifecycle (CAT-02).
"""
def test_create_product_success_and_duplicate_slug(client, admin_headers):
    cat = client.post("/api/v1/admin/categories", json={"name": "Audio Gear", "slug": "audio-gear"}, headers=admin_headers).json()
    
    prod_resp = client.post("/api/v1/admin/products", json={
        "category_id": cat["id"],
        "name": "Studio Pro Headphones",
        "slug": "studio-pro-headphones",
        "description": "Professional closed-back monitor headphones.",
        "status": "draft",
        "specifications": {"impedance_ohms": 80}
    }, headers=admin_headers)
    assert prod_resp.status_code == 201
    assert prod_resp.json()["status"] == "draft"

    # Duplicate slug check (CAT-02, CAT-05)
    dup_resp = client.post("/api/v1/admin/products", json={
        "category_id": cat["id"],
        "name": "Different Name Same Slug",
        "slug": "studio-pro-headphones",
        "description": "Duplicate description"
    }, headers=admin_headers)
    assert dup_resp.status_code == 409

def test_update_product_success(client, admin_headers):
    cat = client.post("/api/v1/admin/categories", json={"name": "Smartphones", "slug": "smartphones"}, headers=admin_headers).json()
    prod = client.post("/api/v1/admin/products", json={
        "category_id": cat["id"],
        "name": "Samsung Galaxy A15",
        "slug": "samsung-galaxy-a15",
        "description": "Initial draft description",
        "status": "draft"
    }, headers=admin_headers).json()

    # Update description and status
    patch_resp = client.patch(f"/api/v1/admin/products/{prod['id']}", json={
        "description": "Updated commercial description with 50MP camera.",
        "status": "published"
    }, headers=admin_headers)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "published"
    assert "50MP camera" in patch_resp.json()["description"]

def test_product_invalid_category_fails(client, admin_headers):
    resp = client.post("/api/v1/admin/products", json={
        "category_id": 999999,
        "name": "Orphan Product",
        "slug": "orphan-product",
        "description": "No parent category exists"
    }, headers=admin_headers)
    assert resp.status_code == 404
