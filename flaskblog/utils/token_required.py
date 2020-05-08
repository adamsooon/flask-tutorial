from flask import request, current_app
from functools import wraps
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            return {'message': 'token is missing'}, 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            print(data)
        except:
            return {'message': 'token is invalid'}, 401

        return f(*args, **kwargs)

    return decorated
