
from email import message
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine,Base
from app.models.user import User
from app.schema.user import UserCreate, UserResponse, UserLogin
from app.auth.securirty import hash_passsword
from app.auth.login import router as login_router
from app.auth.dependencies import get_current_user



app = FastAPI()

app.include_router(login_router)


Base.metadata.create_all(bind=engine)

@app.get("/") 
def honme():
    return{message: "Ai compliance Assistance Api"}

@app.get("/health")
def health_check():
    return{"status": "healthy"}

@app.get("/users")
def get_users():
    return{message: "Users"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    db: Session = SessionLocal()

    hashed_password = hash_passsword(user.password)

    new_user = User(
        name= user.name,
        email=user.email,
        password_hash=hashed_password
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()


    return new_user

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "You are accessing a protected route",
        "user_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email

    }


