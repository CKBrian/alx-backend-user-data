"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
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
        # Create a new session
        session = self._session

        # Create a new User object with the given email and hashed password
        user = User(email=email, hashed_password=hashed_password)

        # Add the new user to the session
        session.add(user)

        # Commit the changes to the database
        session.commit()

        # Return the newly created user object
        return user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
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
            session = self._session
            user = session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound()
        except (InvalidRequestError, NoResultFound) as e:
            raise e
        return user
