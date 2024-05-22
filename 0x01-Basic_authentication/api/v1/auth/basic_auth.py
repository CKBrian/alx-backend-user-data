#!/usr/bin/env python3
'''BasicAuth module'''

from api.v1.auth.auth import Auth
import base64


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
