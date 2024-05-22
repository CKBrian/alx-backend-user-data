#!/usr/bin/env python3
'''BasicAuth module'''

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    '''BasicAuth class'''

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        '''returns the Base64 part of the Authorization
           header for a Basic Authentication'''
        header = authorization_header
        if header and isinstance(header, str) and header.startswith('Basic '):
            return authorization_header[len('Basic '):]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''returns the decoded value of a Base64 string
           base64_authorization_header:'''
        auth_header = base64_authorization_header
        try:
            if not auth_header and not isinstance(auth_header, str):
                None
            decoded = base64.b64decode(auth_header, validate=True)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''returns user email and password from the Base64 decoded value'''
        decoded_auth_header = decoded_base64_authorization_header
        if decoded_auth_header and isinstance(decoded_auth_header, str):
            if ':' in decoded_auth_header:
                email, passwd = decoded_auth_header.split(':')
                return (email, passwd)
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''returns the User instance based on his email and password.'''
        if not user_email and not isinstance(user_email, str):
            return None
        if not user_pwd and not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if users:
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads Auth and retrieves
           the User instance for a request'''
        header = request.headers.get('Authorization', None)
        authorization_header = extract_base64_authorization_header(header)
        decoded_auth_header = decode_base64_authorization_header(
                authorization_header)
        email, passwd = extract_user_credentials(decoded_auth_header)
        user = user_object_from_credentials(email, passwd)
