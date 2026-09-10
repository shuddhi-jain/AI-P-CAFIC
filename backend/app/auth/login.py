from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schema.user import UserLogin
from app.auth.securirty import verify_password
from app.auth.jwt import create_access_token,create_refresh_token, decode_refresh_token


router = APIRouter(
    prefix= "/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user: UserLogin, response: Response):
    db: Session = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        db.close()
        return{"message": "Invalid email or password"}
    
    if not verify_password(user.password, db_user.password_hash):
        db.close()
        return{"message": "Invalid email or password"}

    access_token = create_access_token(db_user.id)
    refresh_token = create_refresh_token(db_user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=15 * 60,
    )

    response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,
        )

    db.close()

    return{
        "message": "Login Successfull",
    }

@router.post("/refreh")
def refresh_access_token(request: Request, respoonse: Response):
    refresh_token = request.cookies.get("refresh_token")

   
    
    
