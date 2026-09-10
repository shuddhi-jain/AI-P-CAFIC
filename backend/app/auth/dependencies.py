from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session                
from app.auth.jwt import decode_access_token
from app.database import get_db
from app.models.user import User

def get_current_user(request: Request,
                     db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    user_id = decode_access_token(access_token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return user
