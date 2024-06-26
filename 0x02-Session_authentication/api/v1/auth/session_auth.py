#!/usr/bin/env python3
'''SessionAuth module'''

from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    '''SessionAuth Class'''

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Return:
                users session Id
        '''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns:
               a User ID based on a Session ID
        '''
        if not session_id or not isinstance(session_id, str):
            return None
        return self.__class__.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''Returns:
               the current user object'''
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''Destroys/ session token or deletes the user session / logout'''
        session_id = self.session_cookie(request)
        if not request or not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            False
        self.user_id_by_session_id.pop(session_id)
        return True
