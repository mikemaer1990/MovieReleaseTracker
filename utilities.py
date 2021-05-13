import functools
from flask import g, flash, redirect, url_for

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please Log In')
            return redirect(url_for('login'))

        return view(**kwargs)
    return wrapped_view

def check_confirmed(func):
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if g.user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function