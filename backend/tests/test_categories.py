"""
Automated tests for Category CRUD, Tree Hierarchy & Cycle Prevention (CAT-01).
"""
def test_create_category_and_parent_assignment(client, admin_headers):
    # 1. Create root category
    resp = client.post("/api/v1/admin/categories", json={
        "name": "Computing & Peripherals",
        "slug": "computing-peripherals",
        "description": "Laptops and desktop computing equipment."
    }, headers=admin_headers)
    assert resp.status_code == 201
    root_id = resp.json()["id"]

    # 2. Create child category
    resp_child = client.post("/api/v1/admin/categories", json={
        "name": "Mechanical Keyboards",
        "slug": "mechanical-keyboards",
        "parent_id": root_id
    }, headers=admin_headers)
    assert resp_child.status_code == 201
    child_id = resp_child.json()["id"]
    assert resp_child.json()["parent_id"] == root_id

    # 3. Retrieve tree
    tree_resp = client.get("/api/v1/admin/categories", headers=admin_headers)
    assert tree_resp.status_code == 200
    tree = tree_resp.json()
    root_node = next((c for c in tree if c["id"] == root_id), None)
    assert root_node is not None
    assert len(root_node["children"]) == 1
    assert root_node["children"][0]["id"] == child_id

def test_category_prevent_circular_dependency(client, admin_headers):
    c1 = client.post("/api/v1/admin/categories", json={"name": "Category Alpha", "slug": "cat-alpha"}, headers=admin_headers).json()
    c2 = client.post("/api/v1/admin/categories", json={"name": "Category Beta", "slug": "cat-beta", "parent_id": c1["id"]}, headers=admin_headers).json()

    # Attempt cycle: make parent A child of B
    cycle_resp = client.patch(f"/api/v1/admin/categories/{c1['id']}", json={"parent_id": c2["id"]}, headers=admin_headers)
    assert cycle_resp.status_code == 400
    assert "Circular dependency detected" in cycle_resp.json()["detail"]

def test_category_duplicate_slug_conflict(client, admin_headers):
    client.post("/api/v1/admin/categories", json={"name": "Category One", "slug": "unique-slug"}, headers=admin_headers)
    resp = client.post("/api/v1/admin/categories", json={"name": "Category Two", "slug": "unique-slug"}, headers=admin_headers)
    assert resp.status_code == 409
