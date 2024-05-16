#!/usr/bin/env python3
'''Defines a module with functions that perform encryption'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''function that expects one string argument name password
       and returns a salted hashed password, which is a byte string.'''
    # bcrypt salt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
