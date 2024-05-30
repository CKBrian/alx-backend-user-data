#!/usr/bin/env python3

'''Defines an Auth module'''

import bcrypt
from db import DB, NoResultFound, User
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Registers a User'''
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User <user's email> already exists")
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        '''Validates a users password'''
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''Returns a users session id'''
        try:
            user = self._db.find_user_by(email=email)
            id = user.id
            session_id = _generate_uuid()
            self._db.update_user(id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        '''Returns a user from session_id'''
        try:
            if not session_id:
                return None
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        '''Destroys a user session'''
        try:
            if not user_id:
                return None
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None


def _hash_password(password: str) -> bytes:
    '''Returns a hashed passwd'''
    if password:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    '''generates a UUID'''
    return str(uuid.uuid4())
