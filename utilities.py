import functools
import configuration
import ipinfo
from flask import g, flash, redirect, url_for
from itsdangerous import URLSafeTimedSerializer

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

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(configuration.SECRET_KEY_STORAGE)
    return serializer.dumps(email, salt = configuration.SECRET_KEY_STORAGE)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(configuration.SECRET_KEY_STORAGE)
    try:
        email = serializer.loads(
            token,
            salt = configuration.SECRET_KEY_STORAGE,
            max_age = expiration
        )
    except:
        return False
    return email

# https://github.com/ipinfo/python
def get_locale():
    access_token = configuration.IPINFO_KEY
    try:
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails()
        return details.country
    except Exception as e:
        print(e)
        return 'US'