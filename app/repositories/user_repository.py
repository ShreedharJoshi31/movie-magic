from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.models import User  # Import your User model
from app.repositories.base import BaseRepository  # Import the BaseRepository


class UserRepository(BaseRepository):
    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """
        Create a new user in the database.

        :param db: Database session
        :param user_data: Dictionary containing user data
        :return: The created User object
        """
        return BaseRepository.create_entry(db=db, model=User, data=user_data)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        :param db: Database session
        :param user_id: ID of the user
        :return: The User object or None if not found
        """
        return BaseRepository.get_entry_by_id(db=db, model=User, id=user_id)

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.

        :param db: Database session
        :param email: Email of the user
        :return: The User object or None if not found
        """
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            raise e

    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        """
        Retrieve all users.

        :param db: Database session
        :return: List of User objects
        """
        return BaseRepository.get_all_entries(db=db, model=User)

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict) -> Optional[User]:
        """
        Update a user's details.

        :param db: Database session
        :param user_id: ID of the user to update
        :param update_data: Dictionary of fields to update
        :return: The updated User object or None if not found
        """
        return BaseRepository.update_entry(db=db, model=User, update_data=update_data, id=user_id)

    @staticmethod
    def soft_delete_user(db: Session, user_id: int) -> Optional[User]:
        """
        Soft delete a user (mark as deleted without removing the record).

        :param db: Database session
        :param user_id: ID of the user to soft delete
        :return: The soft-deleted User object or None if not found
        """
        return BaseRepository.soft_delete_entry(db=db, model=User, id=user_id)

    @staticmethod
    def hard_delete_user(db: Session, user_id: int) -> bool:
        """
        Permanently delete a user from the database.

        :param db: Database session
        :param user_id: ID of the user to delete
        :return: True if deleted, False if not found
        """
        return BaseRepository.hard_delete_entry(db=db, model=User, id=user_id)