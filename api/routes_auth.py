from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

# Request models
class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str

# Global database - make sure this is properly shared
users_db: Dict[str, Dict[str, Any]] = {}

print("🚀 Authentication router initialized!")
print("📝 Current users in database:", list(users_db.keys()))

@router.post("/signup")
async def signup(data: SignUpRequest):
    print(f"\n=== SIGNUP ATTEMPT ===")
    print(f"📧 Email: {data.email}")
    print(f"👤 Username: {data.username}")
    print(f"🔐 Password: {data.password}")
    
    # Convert email to lowercase for consistent comparison
    email_lower = data.email.lower().strip()
    
    # Check if user already exists
    if email_lower in users_db:
        print(f"❌ User already exists: {email_lower}")
        print(f"📊 Current users: {list(users_db.keys())}")
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Store user data
    users_db[email_lower] = {
        "username": data.username.strip(),
        "email": email_lower,
        "password": data.password,
    }
    
    print(f"✅ User successfully registered: {email_lower}")
    print(f"📊 Current users in database: {list(users_db.keys())}")
    print("=== SIGNUP SUCCESS ===\n")
    
    return {"message": "Sign-up successful", "email": email_lower}

@router.post("/signin")
async def signin(data: SignInRequest):
    print(f"\n=== SIGNIN ATTEMPT ===")
    print(f"📧 Email: {data.email}")
    print(f"🔐 Password: {data.password}")
    print(f"📊 Available users: {list(users_db.keys())}")
    
    email_lower = data.email.lower().strip()
    
    user = users_db.get(email_lower)
    
    if not user:
        print(f"❌ User not found: {email_lower}")
        print("=== SIGNIN FAILED ===\n")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Compare passwords
    if user["password"] != data.password:
        print(f"❌ Password mismatch for: {email_lower}")
        print(f"💾 Stored password: {user['password']}")
        print(f"📨 Provided password: {data.password}")
        print("=== SIGNIN FAILED ===\n")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    print(f"✅ Successful signin for: {email_lower}")
    print(f"👤 Welcome: {user['username']}")
    print("=== SIGNIN SUCCESS ===\n")
    return {"message": f"Welcome back, {user['username']}!"}

# Debug endpoint to see all users
@router.get("/debug-users")
async def debug_users():
    return {
        "total_users": len(users_db),
        "users": users_db
    }

# Health check endpoint
@router.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "user_count": len(users_db),
        "users": list(users_db.keys())
    }