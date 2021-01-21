import requests
import json
import configuration
from flask import request
from datetime import datetime


def lookupReleaseDate(id):
    release_obj = None
    digital = None
    theatre = None
    tvDate = None
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}/release_dates?&api_key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        movies = response.json()['results']
        for i in movies:
            if i['iso_3166_1'] == 'US':
                for y in i['release_dates']:
                    if y['type'] == 4:
                        digital = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        digital_full = digital.strftime('%B %d, %Y')
                        digital_small = digital.strftime('%Y-%m-%d')
                    elif y['type'] == 3:
                        theatre = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        theatre_full = theatre.strftime('%B %d, %Y')
                        theatre_small = theatre.strftime('%Y-%m-%d')
                    elif y['type'] == 6:
                        tvDate = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        tvDate_full = tvDate.strftime('%B %d, %Y')
                        tvDate_small = tvDate.strftime('%Y-%m-%d')
        if theatre is None and digital is None:
            if tvDate is None:
                digital_full = 'TBA'
                digital_small = 'TBA'
                theatre_full = 'TBA'
                theatre_small = 'TBA'
            else:
                digital = tvDate
                digital_full = digital.strftime('%B %d, %Y')
                digital_small = digital.strftime('%Y-%m-%d')
        if digital is None:
            digital_full = 'TBA'
            digital_small = 'TBA'
        if theatre is None:
            theatre_full = 'TBA'
            theatre_small = 'TBA'

        release_obj = {
            "digital": {"full": digital_full, "small": digital_small},
            "theatre": {"full": theatre_full, "small": theatre_small}
        }

        return release_obj
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return release_obj


def lookupTrailer(id):
    trailer_url = None
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={api_key}&language=en-US")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        movies = response.json()['results']
        trailer_key = movies[0]['key']
        if trailer_key is not None:
            trailer_url = f"https://www.youtube.com/embed/{trailer_key}"
            return trailer_url
        else:
            return None
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return trailer_url
# function to lookup movie in API via name string


def lookupDirector(id):
    director_name = None
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}/credits?api_key={api_key}&language=en-US")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        directors = []
        # jsonify response
        results = response.json()
        for i in results['crew']:
            if i['job'] == 'Director':
                directors.append(i['name'])
        return directors
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return directors


def lookup(movie):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie}&page=1&include_adult=false&region=US")
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
                "full_release": result["release_date"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"]
            })

            def sort(e):
                return e['release']

            results.sort(reverse=True, key=sort)
        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results


def lookupTv(title):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&language=en-US&page=1&query={title}&include_adult=false")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        shows = response.json()
        # initialize result list
        results = []
        search = shows['results']
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
                "full_release": result["release_date"]
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
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US&region=CA")
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
        release = lookupReleaseDate(movies['id'])
        trailer = lookupTrailer(id)
        director = lookupDirector(id)
        
        # THIS NEEDS WORK CLEARLY 
        if release['digital']['full'] == 'TBA' and release['theatre']['full'] == 'TBA' or not release['digital']['full'] and not release['theatre']['full']:
            date_obj = datetime.strptime(movies["release_date"], '%Y-%m-%d')
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
        elif release['digital']['full'] == 'TBA':
            release_date = release['theatre']['full']
            date_obj = datetime.strptime(
                release['theatre']['small'], '%Y-%m-%d')
        elif release['theatre']['full'] == 'TBA':
            release_date = release['digital']['full']
            date_obj = datetime.strptime(
                release['digital']['small'], '%Y-%m-%d')
        else:
            release_date = release['digital']['full']
            date_obj = datetime.strptime(
                release['digital']['small'], '%Y-%m-%d')
        released = date_obj.date() <= datetime.now().date()

        # create an object and add it to our results list
        results.append({
            "name": movies["original_title"],
            "id": movies["id"],
            "release_small": date_obj.date(),
            "release_full": release_date,
            "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
            "rating": movies["vote_average"],
            "imdb": movies["imdb_id"],
            "released": released,
            "trailer": trailer,
            "overview": movies["overview"],
            "genres": movies["genres"],
            "director": director
        })
        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results


# if __name__ == "__main__":
#     print(lookupTrailer('641662'))
#     print(lookupReleaseDate('464052'))
