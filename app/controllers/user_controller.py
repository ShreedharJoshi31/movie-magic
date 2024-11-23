from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.schemas.schemas import User, Login, UserResponse  # Import your Pydantic schemas
from app.database import get_db  # Dependency to get the database session
from app.utils.auth import verify_password  # Import authentication utilities

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def signup(user_data: User, db: Session = Depends(get_db)) -> User:
    """
    Handle user signup.
    """
    try:
        # Create the user using the service layer
        new_user = UserService.create_user(db=db, user_data=user_data.model_dump())
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def login(user_credentials: Login, db: Session = Depends(get_db)) -> dict:
    """
    Handle user login.
    """
    # Retrieve the user by email
    user = UserService.get_user_by_email(db=db, email=user_credentials.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    # Verify the password
    if user_credentials.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )
    
    # Convert SQLAlchemy model to dict first
    user_dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "location": user.location
    }
    
    # Now validate the dict
    user_response = UserResponse.model_validate(user_dict)
    
    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "user": user_response.model_dump()
        }
    }


async def logout(response: Response) -> dict:
    """
    Handle user logout.
    Simple implementation that just clears the cookie.
    """
    # Clear all possible auth cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    
    # Clear with additional security parameters
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    
    return {
        "status": "success",
        "message": "Logged out successfully",
        "data": None
    }