#!/usr/bin/env python3

'''Defines an app module'''
from flask import (
        Flask, jsonify, request, abort,
        make_response, url_for, redirect)
from auth import Auth

app = Flask('__name__')
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome():
    '''Returns a json payload'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def create_user():
    '''Registers a user'''
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        AUTH.register_user(email, password)
        return jsonify({"email": "<registered email>",
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    '''Validates a user and assigns a session_id'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if session_id:
        resp = make_response(jsonify({"email": "<user email>",
                                      "message": "logged in"}))
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''Logs out the current user'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        resp = redirect(url_for('welcome'))
        return resp
    abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    '''Returns a user profile as json payload'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    try:
        email = request.form.get('email')
        reset_token = get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
