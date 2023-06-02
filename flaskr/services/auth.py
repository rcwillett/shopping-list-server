import functools
from flask import session

def login_required(route):
    @functools.wraps(route)
    def wrapped_route(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return 'Unauthorized', 401
        return route(*args, **kwargs)
    return wrapped_route