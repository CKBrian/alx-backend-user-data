#!/usr/bin/env python3

'''Defines an app module'''
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask('__name__')
AUTH = Auth()


@app.route('/', methods=['GET'])
def get_user():
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
def get_session():
    '''Validates a user and assigns a session_id'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if session_id:
        resp = make_response(jsonify({"email": "<user email>",
                                      "message": "logged in"}))
        resp.create_cookies('session_id', session_id)
        return resp
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
