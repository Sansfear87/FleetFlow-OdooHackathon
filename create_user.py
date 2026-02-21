"""
Run this ONCE after setup to create your admin user.
Usage: python create_user.py
"""
from dotenv import load_dotenv
load_dotenv()
from database import SessionLocal
from models.user import User
from core.security import hash_password

db = SessionLocal()
existing = db.query(User).filter(User.email == "admin@fleetflow.com").first()
if existing:
    print("User already exists: admin@fleetflow.com / admin1234")
else:
    user = User(email="admin@fleetflow.com", password_hash=hash_password("admin1234"), full_name="Fleet Admin", is_active=True)
    db.add(user); db.commit()
    print("Created user: admin@fleetflow.com / admin1234")
db.close()
