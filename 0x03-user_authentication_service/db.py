"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


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
