"""
Standalone seed script — run this ONCE before starting the server.
  python seed.py
"""
import os
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ── Auto-create database if it doesn't exist ─────────────────
if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
    print(f"Database created: {DATABASE_URL}")
else:
    print("Database already exists")

# ── Create engine + tables ────────────────────────────────────
engine = create_engine(DATABASE_URL)

from app.models import Base
Base.metadata.create_all(bind=engine)
print("Tables created")

# ── Seed data ─────────────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    from app.seed_logic import seed_database
    message = seed_database(db)
    print(message)
except Exception as e:
    db.rollback()
    print(f"Seeding failed: {e}")
    raise
finally:
    db.close()

print("Database seeded successfully!")
