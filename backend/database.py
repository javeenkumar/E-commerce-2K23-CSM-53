import os
from sqlalchemy import create_engine, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./catalog.db")

# Use StaticPool or check_same_thread=False for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Flexible JSON type: uses JSONB on PostgreSQL and JSON on SQLite
FlexibleJSON = JSON().with_variant(JSONB, "postgresql")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
