#!/usr/bin/env python3
'''Auth module
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''Auth class'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns False if a path is in excluded_paths
        '''
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            return (False if path in excluded_paths or f'{path}/'
                    in excluded_paths else True)
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        '''that returns None - request'''
        headers = request.headers
        return (headers.get('Authorization', None)
                if headers else None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''that returns None - request'''
        return request