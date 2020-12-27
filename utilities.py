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