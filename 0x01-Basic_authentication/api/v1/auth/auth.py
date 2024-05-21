api/v1/auth/auth.py
'''Auth module
'''
from flaskimport request


class Auth:
    '''Auth class'''
    def require_auth(self, path: str, excluded_paths:List[str]) -> bool:
       '''returns False - path
       '''
       return False

    def authorization_header(self, request=None) -> str:
       '''that returns None - request'''
       return request

    def current_user(self, request=None) -> TypeVar('User'):
        '''that returns None - request'''
        return request
