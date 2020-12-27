# sensitive variables imported here from os
import os

API_KEY_STORAGE = os.environ.get('TMDB_API_KEY')
SECRET_KEY_STORAGE = os.environ.get('SECRET_KEY')
EMAIL_USERNAME = os.environ.get('MOVIE_EMAIL')
EMAIL_PASSWORD = os.environ.get('MOVIE_PASS')
DATABASE_URL = os.environ.get('DATABASE_URL')