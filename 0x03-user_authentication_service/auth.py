#!/usr/bin/env python3

'''Defines an Auth module'''

import bcrypt
from db import DB, NoResultFound, User


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


def _hash_password(password: str) -> bytes:
    '''Returns a hashed passwd'''
    if password:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
