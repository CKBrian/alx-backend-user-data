#!/usr/bin/env python3
"""
Main file
"""
import requests
import json


home = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    '''Registers a new user'''
    data = {'email': email, 'password': password}
    url = f'{home}/users'
    resp = requests.post(url, data=data)
    assert resp.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Validates a user"""
    data = {'email': email, 'password': password}
    url = f'{home}/sessions'
    resp = requests.post(url, data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    '''validates and logs in a user'''
    data = {'email': email, 'password': password}
    url = f'{home}/sessions'
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    return resp.cookies.get_dict().get('session_id')


def profile_unlogged() -> None:
    '''Unlogs a useer profile'''
    url = f'{home}/profile'
    resp = requests.get(url)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Returns a users profile'''
    url = f'{home}/profile'
    cookies = {'session_id': session_id}
    resp = requests.get(url, cookies=cookies)
    assert resp.status_code == 200


def log_out(session_id: str) -> None:
    '''Logs out a user'''
    url = f'{home}/sessions'
    cookies = {'session_id': session_id}
    resp = requests.delete(url, cookies=cookies)
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    '''Resets a password token'''
    data = {'email': email}
    cookies = {'session_id': session_id}
    url = f'{home}/reset_password'
    resp = requests.post(url, data=data, cookies=cookies)
    assert resp.status_code == 200
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''updates a users password'''
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    cookies = {'session_id': session_id}
    url = f'{home}/reset_password'
    resp = requests.put(url, data=data, cookies=cookies)
    assert resp.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
