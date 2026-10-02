"""
FastAPI Main Application for Sprint 2 Catalog Data Foundation.
Mounts administrative routers for Categories, Products, and SKUs under /api/v1/admin.
"""
from fastapi import FastAPI
from backend.database import Base, engine
from backend.routes.categories import router as categories_router
from backend.routes.products import router as products_router
from backend.routes.skus import router as skus_router

# Ensure tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Catalog API - Sprint 2",
    description="Administrative catalog foundation with strict relational integrity and RBAC",
    version="2.0.0"
)

# Mount all administrative routers with required prefix
app.include_router(categories_router, prefix="/api/v1/admin")
app.include_router(products_router, prefix="/api/v1/admin")
app.include_router(skus_router, prefix="/api/v1/admin")

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "sprint": "Sprint 2 - Catalog Data Foundation",
        "author": "Javeen Kumar (2K23/CSM/53)"
    }
