# Sprint 1: Architecture & Scope Definition
**Name:** Javeen Kumar  
**Roll No.:** 2K23/CSM/53

---

## Section 1: Target Audience & Market Focus

* **Primary Persona:** Tech-savvy urban retail consumers and university professionals seeking quick, reliable access to consumer electronics, smart accessories, and computing peripherals.
* **Core Pain Point:** Fragmented online shopping experiences, lack of real-time inventory visibility, unreliable order tracking, and sluggish checkout workflows.
* **Domain Scope:** Consumer Electronics & Gadgets E-Commerce.

---

## Section 2: Minimum Viable Product (MVP) Feature Scope

| Category | Feature Name | Description | Priority |
| :--- | :--- | :--- | :--- |
| **Authentication** | User Registration & Authentication | Secure password hashing (bcrypt) and JWT-based session authentication mechanism. | High (MVP) |
| **Catalog** | Product List & Search | Dynamic product browsing interface equipped with taxonomy-based filtering and keyword search. | High (MVP) |
| **Cart** | Cart Management | State-persistent cart management supporting item addition, quantity modification, and item deletion. | High (MVP) |
| **Checkout** | Order Processing | Stripe payment gateway integration and order object instantiation with status tracking. | High (MVP) |
| **Admin** | Inventory Control | Administrative dashboard enabling full CRUD operations for product catalog and inventory management. | Medium |

---

## Section 3: Tech Stack Selection & Justification

* **Frontend Framework:** Flutter (Web & Cross-Platform)
  * *Justification:* Utilizing Flutter for the web allows a unified Dart codebase to deliver a responsive, highly fluid UI experience across desktop and mobile browsers. Combined with Provider for state management, it ensures smooth rendering of dynamic product lists and seamless real-time cart updates.
* **Backend Infrastructure:** Python FastAPI
  * *Justification:* FastAPI provides high-performance, asynchronous endpoints with automatic Swagger documentation validation. Its lightweight structure and fast execution speed make it ideal for building robust, scalable e-commerce REST APIs consumed directly by the Flutter client.
* **Database Management System:** PostgreSQL
  * *Justification:* A robust relational database management system that ensures strict data integrity through ACID compliance. It handles complex relational queries between users, orders, and inventory items far more reliably than non-relational alternatives for transactional e-commerce models.
* **Caching & Asynchronous Processing:** Redis (Optional)
  * *Justification:* Utilized for fast session store management and caching frequent product catalog queries, drastically reducing database read loads during high-traffic simulations.

---

## Section 4: Entity-Relationship Diagram (ERD)

The relational schema maps out users, categories, products, shopping carts, cart items, orders, and order items with explicit primary keys (PK), foreign keys (FK), and cardinality constraints.

```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    USERS ||--o| CARTS : has
    CATEGORIES ||--o{ PRODUCTS : categorizes
    PRODUCTS ||--o{ ORDER_ITEMS : ordered_in
    PRODUCTS ||--o{ CART_ITEMS : added_to
    ORDERS ||--|{ ORDER_ITEMS : contains
    CARTS ||--o{ CART_ITEMS : holds

    USERS {
        int id PK
        string username
        string email
        string password_hash
        timestamp created_at
    }

    CATEGORIES {
        int id PK
        string name
        string description
    }

    PRODUCTS {
        int id PK
        int category_id FK
        string name
        text description
        decimal price
        int stock_quantity
        string image_url
    }

    CARTS {
        int id PK
        int user_id FK
        timestamp updated_at
    }

    CART_ITEMS {
        int id PK
        int cart_id FK
        int product_id FK
        int quantity
    }

    ORDERS {
        int id PK
        int user_id FK
        decimal total_amount
        string status
        timestamp created_at
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }