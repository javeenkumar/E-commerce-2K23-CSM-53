"""
Automated tests for Administrative Access Control (CAT-06).
"""
def test_admin_auth_rejection_unauthenticated(client):
    resp = client.post("/api/v1/admin/categories", json={"name": "Fail Category", "slug": "fail-slug"})
    assert resp.status_code == 401
    assert "Missing Authorization header" in resp.json()["detail"]

def test_admin_auth_rejection_regular_user(client, customer_headers):
    resp = client.post("/api/v1/admin/categories", json={"name": "Fail Category", "slug": "fail-slug"}, headers=customer_headers)
    assert resp.status_code == 403
    assert "Administrative privilege required" in resp.json()["detail"]

def test_admin_auth_allowed_for_admin_user(client, admin_headers):
    resp = client.post("/api/v1/admin/categories", json={"name": "Auth Success", "slug": "auth-success"}, headers=admin_headers)
    assert resp.status_code == 201
    assert resp.json()["slug"] == "auth-success"
