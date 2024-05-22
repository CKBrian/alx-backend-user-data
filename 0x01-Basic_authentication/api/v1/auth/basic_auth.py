#!/usr/bin/env python3
'''BasicAuth module'''

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''BasicAuth class'''

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        '''returns the Base64 part of the Authorization
        header for a Basic Authentication'''
        header = authorization_header
        if header and type(header) is 'str' and header.startswith('Basic'):
            return header.split('Basic ')
        return None
