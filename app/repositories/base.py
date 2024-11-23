from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, TypeVar, List, Optional, Any
from sqlalchemy import and_
from sqlalchemy.inspection import inspect

# Type hint for SQLAlchemy ORM models
T = TypeVar("T")

class BaseRepository:
    @staticmethod
    def _get_primary_key_filters(model: Type[T], **pk_kwargs) -> Any:
        """
        Builds a SQLAlchemy filter condition based on the primary keys of the model.

        :param model: The SQLAlchemy model class.
        :param pk_kwargs: Keyword arguments representing primary key fields and their values.
        :return: A SQLAlchemy filter condition.
        """
        mapper = inspect(model)
        primary_keys = mapper.primary_key

        if len(pk_kwargs) != len(primary_keys):
            raise ValueError(
                f"Expected {len(primary_keys)} primary key(s), got {len(pk_kwargs)}."
            )

        conditions = []
        for key in primary_keys:
            key_name = key.name
            if key_name not in pk_kwargs:
                raise ValueError(f"Missing value for primary key field '{key_name}'.")
            conditions.append(getattr(model, key_name) == pk_kwargs[key_name])

        return and_(*conditions)
    
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

    def get_entry_by_id(db: Session, model: Type[T], check_soft_delete: bool = True, **pk_kwargs) -> Optional[T]:
        """
        Retrieve a single entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param **pk_kwargs: ID of the entry
        :return: The entry or None if not found
        """
        try:
            query = db.query(model)

            # Dynamically check for soft_delete attribute
            if hasattr(model, 'soft_delete'):
                query = query.filter(model.soft_delete == (not check_soft_delete))

            filter_condition = BaseRepository._get_primary_key_filters(model, **pk_kwargs)
            return query.filter(filter_condition).first()
        except SQLAlchemyError as e:
            raise e

    def get_all_entries(db: Session, model: Type[T], check_soft_delete: bool = True) -> List[T]:
        """
        Retrieve all entries of a specific model.
        
        :param db: Database session
        :param model: The model class
        :return: List of entries
        """
        return db.query(model).filter(model.soft_delete == (not check_soft_delete)).all()

    def update_entry(db: Session, model: Type[T], update_data: dict, **pk_kwargs) -> Optional[T]:
        """
        Update an entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param **pk_kwargs: ID of the entry to update
        :param update_data: Dictionary of fields to update
        :return: The updated entry or None if not found
        """
        
        try:
            entry = BaseRepository.get_entry_by_id(db=db, model=model, **pk_kwargs)
            if not entry:
                return None
            for key, value in update_data.items():
                setattr(entry, key, value)
            db.commit()
            db.refresh(entry)
            return entry
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        
    
    def soft_delete_entry(db: Session, model: Type[T], **pk_kwargs) -> Optional[T]:
        """
        Soft delete an entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param **pk_kwargs: ID of the entry to delete
        :return: The soft-deleted entry or None if not found
        """
        
        if(not hasattr(model, 'soft_delete')):
            raise ValueError(f"{model} does not have a soft_delete attribute")
        
        
        try:
            entry = BaseRepository.get_entry_by_id(db=db, model=model, **pk_kwargs)
            if not entry:
                return None
            entry.soft_delete = True
            db.commit()
            db.refresh(entry)
            return entry
        except SQLAlchemyError as e:
            db.rollback()

    def hard_delete_entry(db: Session, model: Type[T], **pk_kwargs) -> bool:
        """
        Delete an entry by its ID.
        
        :param db: Database session
        :param model: The model class
        :param **pk_kwargs: ID of the entry to delete
        :return: True if deleted, False if not found
        """

        try:
            entry = BaseRepository.get_entry_by_id(db=db, model=model, **pk_kwargs)
            if not entry:
                return False
            db.delete(entry)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise e
