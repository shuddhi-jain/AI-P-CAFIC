from fastapi import APIRouter, Request, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schema.user import UserLogin
from app.auth.securirty import verify_password
from app.auth.jwt import create_access_token,create_refresh_token, decode_refresh_token


router = APIRouter(
    prefix= "/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user: UserLogin, response: Response,
          db: Session = Depends(get_db)):
    

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
          raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password"
                )
    
    if not verify_password(user.password, db_user.password_hash):
          raise HTTPException(
                         status_code=401,
                         detail="Invalid email or password"
                     )

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


    return{
        "message": "Login Successfull",
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token"
    )

    response.delete_cookie(
        key="refresh_token"
    )

    return{
        "message": "Logout successfull"
    }

@router.post("/refresh")
def refresh_access_token(request: Request, respoonse: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )

    user_id = decode_refresh_token(refresh_token)

    if not user_id:
        raise HTTPException(
              status_code=401,
              detail="Invalid or expired refresh token"
        )

    new_access_token = create_access_token(int(user_id))

    respoonse.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=15*60,
    )

    return{
        "message": "Access token refreshed"
    }

    
    
