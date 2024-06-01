#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, Any
import logging

from user import Base, User
logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The hashed password for the user.

        Returns:
            User: The newly created user object.
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by the given keyword arguments.

        Args:
            **kwargs: columns and their values to filter by.

        Returns:
            User: The user object matching the given keyword arguments.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If there is an invalid request.
        """
        try:
            for key, val in kwargs.items():
                if not hasattr(User, key):
                    raise InvalidRequestError()
            session = self._session
            user = session.query(User).filter_by(**kwargs).one()
        except (InvalidRequestError, NoResultFound) as e:
            raise e
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user by the given keyword arguments.

        Args:
            **kwargs: columns and their values to filter by.

        Returns:
            User: The user object matching the given keyword arguments.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If there is an invalid request.
        """
        try:
            attrs = [column.key for column in inspect(User).columns]
            user = self.find_user_by(id=user_id)
            for key, val in kwargs.items():
                if not hasattr(User, key):
                    raise ValueError()
                setattr(user, key, val)
            self._session.commit()
        except ValueError as e:
            self._session.rollback()
            raise e
