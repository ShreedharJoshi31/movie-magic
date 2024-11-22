from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.schemas.schemas import UserCreate, UserLogin, UserOut
from app.database import get_db

router = APIRouter()

def signup(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        created_user = service.signup(user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def login(user_login: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.login(user_login)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def logout(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.logout()
