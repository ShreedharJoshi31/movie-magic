from sqlalchemy.orm import Session
from app.schemas.models import User
from app.schemas.schemas import UserCreate
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username, email=user.email, password=hashed_password, location=user.location)
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise ValueError("Email or username already exists.")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
