#!/usr/bin/env python3
'''Defines a route module for the API login'''

from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_authentication():
    '''Handles user authentication'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = make_response(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    resp.set_cookie(session_name, session_id)
    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def user_sign_out():
    '''Handles user authentication'''
    from api.v1.app import auth
    status = auth.destroy_session(request)
    if not status:
        abort(404)
    return jsonify({}), 200
