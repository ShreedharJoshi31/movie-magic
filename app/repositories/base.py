from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, TypeVar, List, Optional

# Type hint for SQLAlchemy ORM models
T = TypeVar("T")

class BaseRepository:
    def create_entry(db: Session, model: Type[T], data: dict) -> T:
        """
        Create a new entry in the database.
        
        :param db: Database session
        :param model: The model class
        :param data: Dictionary containing the data for the new entry
        :return: The created entry
        """
        try:
            entry = model(**data)
            db.add(entry)
            db.commit()
            db.refresh(entry)
            return entry
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def get_entry_by_id(db: Session, model: Type[T], entry_id: int, check_soft_delete: bool = True) -> Optional[T]:
        """
        Retrieve a single entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param entry_id: ID of the entry
        :return: The entry or None if not found
        """
        return db.query(model).filter(model.id == entry_id, model.soft_delete == (not check_soft_delete)).first()

    def get_all_entries(db: Session, model: Type[T], check_soft_delete: bool = True) -> List[T]:
        """
        Retrieve all entries of a specific model.
        
        :param db: Database session
        :param model: The model class
        :return: List of entries
        """
        return db.query(model).filter(model.soft_delete == (not check_soft_delete)).all()

    def update_entry(db: Session, model: Type[T], entry_id: int, update_data: dict) -> Optional[T]:
        """
        Update an entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param entry_id: ID of the entry to update
        :param update_data: Dictionary of fields to update
        :return: The updated entry or None if not found
        """
        entry = db.query(model).filter(model.id == entry_id).first()
        if not entry:
            return None
        
        try:
            for key, value in update_data.items():
                setattr(entry, key, value)
            db.commit()
            db.refresh(entry)
            return entry
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        
    
    def soft_delete_entry(db: Session, model: Type[T], entry_id: int) -> Optional[T]:
        """
        Soft delete an entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param entry_id: ID of the entry to delete
        :return: The soft-deleted entry or None if not found
        """
        entry = db.query(model).filter(model.id == entry_id).first()
        if not entry:
            return None
        
        try:
            entry.soft_delete = True
            db.commit()
            db.refresh(entry)
            return entry
        except SQLAlchemyError as e:
            db.rollback()

    def hard_delete_entry(db: Session, model: Type[T], entry_id: int) -> bool:
        """
        Delete an entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param entry_id: ID of the entry to delete
        :return: True if deleted, False if not found
        """
        entry = db.query(model).filter(model.id == entry_id).first()
        if not entry:
            return False

        try:
            db.delete(entry)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise e
