from sqlalchemy.orm import Session
from typing import Optional, List
from app.repositories.user_repository import UserRepository  # Import the UserRepository
from app.schemas.models import User  # Import your User model


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """
        Create a new user after applying any business logic.

        :param db: Database session
        :param user_data: Dictionary containing user data
        :return: The created User object
        """
        # Example: Check if the email already exists
        existing_user = UserRepository.get_user_by_email(db=db, email=user_data["email"])
        if existing_user:
            raise ValueError("A user with this email already exists.")

        # Proceed to create a new user
        return UserRepository.create_user(db=db, user_data=user_data)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        :param db: Database session
        :param user_id: ID of the user
        :return: The User object or None if not found
        """
        user = UserRepository.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise ValueError(f"No user found with ID {user_id}.")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.

        :param db: Database session
        :param email: Email of the user
        :return: The User object or None if not found
        """
        user = UserRepository.get_user_by_email(db=db, email=email)
        if not user:
            raise ValueError(f"No user found with email {email}.")
        return user

    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        """
        Retrieve all users from the database.

        :param db: Database session
        :return: List of User objects
        """
        return UserRepository.get_all_users(db=db)

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict) -> User:
        """
        Update a user's details.

        :param db: Database session
        :param user_id: ID of the user to update
        :param update_data: Dictionary of fields to update
        :return: The updated User object
        """
        # Check if the user exists
        user = UserRepository.get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise ValueError(f"No user found with ID {user_id}.")

        # Example: Prevent updating the email to one that already exists
        if "email" in update_data:
            existing_user = UserRepository.get_user_by_email(db=db, email=update_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("A user with this email already exists.")

        # Update the user
        return UserRepository.update_user(db=db, user_id=user_id, update_data=update_data)

    @staticmethod
    def soft_delete_user(db: Session, user_id: int) -> User:
        """
        Soft delete a user (mark as deleted without removing the record).

        :param db: Database session
        :param user_id: ID of the user to soft delete
        :return: The soft-deleted User object
        """
        user = UserRepository.soft_delete_user(db=db, user_id=user_id)
        if not user:
            raise ValueError(f"No user found with ID {user_id}.")
        return user

    @staticmethod
    def hard_delete_user(db: Session, user_id: int) -> bool:
        """
        Permanently delete a user from the database.

        :param db: Database session
        :param user_id: ID of the user to delete
        :return: True if deleted, False if not found
        """
        deleted = UserRepository.hard_delete_user(db=db, user_id=user_id)
        if not deleted:
            raise ValueError(f"No user found with ID {user_id}.")
        return deleted