from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schema.user import UserLogin
from app.auth.securirty import verify_password


router = APIRouter(
    prefix= "/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user: UserLogin):
    db: Session = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        db.close()
        return{"message": "Invalid email or password"}
    
    if not verify_password(user.password, db_user.password_hash):
        db.close()
        return{"message": "Invalid email or password"}

    db.close()

    return{
        "message": "Login Successfull",
        "user_id": db_user.id
    }
    
