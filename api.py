import requests
import json
import configuration
from flask import request
from datetime import datetime

# function to lookup movie in API via name string
def lookup(movie):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie}&page=1&include_adult=true")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        movies = response.json()
        # initialize result list
        results = []
        search = movies['results']
        # for each result - store their data in a new list
        for result in search:
            cover = result["poster_path"]
            # parse release date info
            date_obj = datetime.strptime(result["release_date"], '%Y-%m-%d')
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            results.append({
                "name": result["original_title"],
                "id": result["id"],
                "release": release_year,
                "cover" : f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"],
                "overview" : result["overview"]
            })
        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results

# function to lookup movies by id
def lookupById(id):
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US")    
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        movies = response.json()
        # initialize result list
        results = []
        # pre-set cover to be used in f string
        cover = movies["poster_path"]
        # parse release date info
        date_obj = datetime.strptime(movies["release_date"], '%Y-%m-%d')
        release_date = date_obj.strftime('%B %d, %Y')
        released = date_obj.date() < datetime.now().date()
        # create an object and add it to our results list
        results.append({
            "name": movies["original_title"],
            "id": movies["id"],
            "release_date" : movies["release_date"],
            "release": release_date,
            "cover" : f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
            "rating": movies["vote_average"],
            "imdb": movies["imdb_id"],
            "released" : released
        })

        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results