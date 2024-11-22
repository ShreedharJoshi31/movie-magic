from app.repositories.user_repository import UserRepository
from app.schemas.schemas import UserCreate, UserLogin
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def signup(self, user: UserCreate):
        return UserRepository.create_user(self.db, user)

    def login(self, user_login: UserLogin):
        user = UserRepository.get_user_by_email(self.db, user_login.email)
        if user and UserRepository.verify_password(user_login.password, user.password):
            return user
        return None

    def logout(self):
        # Logout logic would depend on your auth implementation
        # You could use JWT or sessions for handling logout
        return {"message": "User logged out successfully"}
