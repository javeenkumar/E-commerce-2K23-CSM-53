# E-Commerce Platform - Sprint 2: Catalog Data Foundation

**Author:** Javeen Kumar  
**Roll No.:** 2K23/CSM/53  
**Course:** E-Commerce  
**Department:** Computer Science / Artificial Intelligence, University of Sindh, Jamshoro  

---

## 1. Project Overview
Sprint 2 implements the transactional catalog data foundation for consumer electronics e-commerce using Python FastAPI, SQLAlchemy, and Pydantic v2. It enforces category tree hierarchies, product containers, variant dimensions, and sellable SKUs with database check constraints, unique indexes, and role-based administrative access control.

---

## 2. Directory Structure

```text
project_ecommerce/
│
├── docs/
│   └── SPRINT_2.md             # Complete Sprint 2 documentation & ERD
│
├── backend/
│   ├── models/                 # SQLAlchemy database models & constraints
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── variant.py
│   │   ├── sku.py
│   │   └── asset.py
│   │
│   ├── routes/                 # Administrative API endpoint handlers
│   │   ├── categories.py
│   │   ├── products.py
│   │   └── skus.py
│   │
│   ├── tests/                  # Automated pytest test suites
│   │   ├── conftest.py
│   │   ├── test_categories.py
│   │   ├── test_products.py
│   │   ├── test_skus.py
│   │   └── test_auth.py
│   │
│   ├── auth.py                 # Admin JWT RBAC dependency (CAT-06)
│   ├── schemas.py              # Pydantic v2 request/response schemas
│   ├── seed.py                 # Reproducible seed data script
│   ├── database.py             # Engine, sessionmaker, and Base
│   └── main.py                 # FastAPI application mount
│
├── .env                        # Local environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # Setup guide and instructions
```

---

## 3. Local Environment Setup

### 3.1 Prerequisites
* Python 3.10+
* Virtual environment tool (`venv`)

### 3.2 Installation
```bash
# Enter project directory
cd project_ecommerce

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3.3 Environment Variables
Configuration is handled via `.env`:
```ini
DATABASE_URL=sqlite:///./catalog.db
SECRET_KEY=dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
*(For production PostgreSQL, set `DATABASE_URL=postgresql://user:pass@localhost:5432/ecommerce_db`)*.

---

## 4. Database Seed Data

Run the reproducible catalog seeder to populate 2 levels of categories, 3 products, and 4 SKUs with 1 intentionally omitted variant combination:
```bash
python -m backend.seed
```

---

## 5. Running Automated Tests

Run the full test suite verifying **CAT-01** to **CAT-06** across all modules:
```bash
python -m pytest -v backend/tests/
```

Expected output:
```text
backend/tests/test_auth.py::test_admin_auth_rejection_unauthenticated PASSED
backend/tests/test_auth.py::test_admin_auth_rejection_regular_user PASSED
backend/tests/test_categories.py::test_create_category_and_parent_assignment PASSED
backend/tests/test_categories.py::test_category_prevent_circular_dependency PASSED
backend/tests/test_categories.py::test_category_duplicate_slug_conflict PASSED
backend/tests/test_products.py::test_create_product_success_and_duplicate_slug PASSED
backend/tests/test_products.py::test_product_invalid_category_fails PASSED
backend/tests/test_skus.py::test_sku_creation_and_duplicate_code_conflict PASSED
backend/tests/test_skus.py::test_sku_negative_stock_rejection PASSED
backend/tests/test_skus.py::test_sku_missing_combinations_omitted PASSED

======================= 10 passed in 0.49s =======================
```

---

## 6. Running the API Server

Start the FastAPI development server:
```bash
uvicorn backend.main:app --reload
```
Interactive Swagger API documentation is available at:
`http://127.0.0.1:8000/docs`
