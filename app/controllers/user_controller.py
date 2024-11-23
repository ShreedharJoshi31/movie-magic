from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.schemas.schemas import User  # Import your Pydantic schemas
from app.database import get_db  # Dependency to get the database session
from app.utils.auth import verify_password  # Import authentication utilities


async def signup(user_data: User, db: Session = Depends(get_db)) -> User:
    """
    Handle user signup.
    """
    try:
        # Create the user using the service layer
        new_user = UserService.create_user(db=db, user_data=user_data.dict())
        return User.model_validate(new_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def login(user_credentials: User, db: Session = Depends(get_db)) -> dict:
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
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    # Generate an access token
    # access_token = create_access_token({"sub": user.email})
    return {"user": User.model_validate(user)}


async def logout() -> dict:
    """
    Handle user logout.
    """
    # In traditional token-based systems, logout is handled client-side by discarding the token.
    # For a more advanced solution (e.g., token invalidation), implement token blacklisting.
    return {"message": "Logged out successfully."}