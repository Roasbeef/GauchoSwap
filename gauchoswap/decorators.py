from functools import wraps
from flask import (session, request, redirect, url_for, flash)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            flash('You must be logged in to do that!', category='error')
            return redirect(url_for('account.fb_auth', after=request.path))
        return f(*args, **kwargs)
    return decorated_function
