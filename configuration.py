import os

API_KEY_STORAGE = os.environ.get('TMDB_API_KEY')
SECRET_KEY_STORAGE = os.environ.get('SECRET_KEY')
EMAIL_USERNAME = os.environ.get('MOVIE_EMAIL')
EMAIL_PASSWORD = os.environ.get('MOVIE_PASS')

# DB_HOST = os.environ.get('DB_HOST')
# DB_USER = os.environ.get('DB_USER')
# DB_PASSWORD = os.environ.get('DB_PASSWORD')
# DB_NAME = os.environ.get('DB_NAME')

DB_HOST = "localhost"
DB_DATABASE = "movie"
DB_USER = "postgres"
DB_PASS = "Cuntfuck123"