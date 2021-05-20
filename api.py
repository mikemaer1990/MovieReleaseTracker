import requests
import json
import configuration
from flask import request
from datetime import datetime

def multiSearch(query, page=1):
        # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&language=en-US&query={query}&page={page}&include_adult=false&region=US")
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
            if 'original_language' in result and result['original_language'] == 'hi':
                continue
            if result['media_type'] == 'movie':
                if result['release_date'] == '' or 'release_date' not in result:
                    date_obj = 'Unknown'
                    release_year = 'Unknown'
                else:
                    # parse release date info
                    date_obj = datetime.strptime(
                    result["release_date"], '%Y-%m-%d')
                    name = result['original_title']
                    release_year = date_obj.strftime('%Y')
                    cover = result["poster_path"]
                    rating = result['vote_average']
            elif result['media_type'] == 'tv':
                if result['first_air_date'] == '' or 'first_air_date' not in result:
                    date_obj = 'Unknown'
                    release_year = 'Unknown'
                else:
                    date_obj = datetime.strptime(
                    result["first_air_date"], '%Y-%m-%d')
                    name = result['original_name']
                    release_year = date_obj.strftime('%Y')
                    cover = result["poster_path"]
                    rating = result['vote_average']
            elif result['media_type'] == 'person':
                date_obj = 'N/A'
                release_year = 'N/A'
                name = result['name']
                cover = result["profile_path"]
                rating = None
            # create an object and add it to our results list
            results.append({
                "type": result["media_type"],
                "name": name,
                "id": result["id"],
                "release": release_year,
                "full_release": date_obj,
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": rating
            })
            # def sort(e):
            #     return e['release']
            # results.sort(reverse=True, key=sort)
        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results

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
                    # Added to fix errors due to release date info being innacurate -> THANKS CORONAVIRUS
                    elif y['type'] == 2 and not tvDate:
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
        print(release_obj)
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


def lookupRelatedMovies(id):
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}/recommendations?api_key={api_key}&language=en-US&page=1")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        movies = response.json()['results']
        relatedList = []
        # for each result - store their data in a new list
        for result in movies:
            cover = result["poster_path"]
            # create an object and add it to our results list
            relatedList.append({
                "name": result["original_title"],
                "id": result["id"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "mediaType": "movie",
                "popularity": result["popularity"]
            })
        return relatedList
        
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return relatedList


def lookupRelatedTv(id):
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/tv/{id}/similar?api_key={api_key}&language=en-US&page=1")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        shows = response.json()['results']
        relatedList = []
        # for each result - store their data in a new list
        for result in shows:
            cover = result["poster_path"]
            # create an object and add it to our results list
            relatedList.append({
                "name": result["original_name"],
                "id": result["id"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "mediaType": "tv",
                "popularity": result["popularity"]
            })

        return relatedList
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return relatedList


def lookupRelated(id):
    movies = lookupRelatedMovies(id)
    tv = lookupRelatedTv(id)
    related = []
    if movies is not None:
        for movie in movies:
            related.append(movie)
    if tv is not None:
        for show in tv:
            related.append(show)

    def sort(e):
        return e['popularity']
    related.sort(reverse=False, key=sort)
    return related


def lookupUpcoming(page=1):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-US&page={page}&region=US")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        search = response.json()['results']
        # initialize result list
        upcomingList = []
        # for each result - store their data in a new list
        for result in search:
            cover = result["poster_path"]
            # parse release date info
            # NEED TO FIX THIS -> IF THE RELEASE DATE INFO IS INACCURATE
            date_obj = datetime.strptime(result["release_date"], '%Y-%m-%d')
            if str(datetime.now().date()) > str(date_obj):
                date_obj = lookupReleaseDate(result["id"])
                continue
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            upcomingList.append({
                "name": result["original_title"],
                "id": result["id"],
                "release": release_year,
                "full_release": release_date,
                "date_obj": date_obj,
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}'
            })

            def sort(e):
                return e['date_obj']

            upcomingList.sort(reverse=False, key=sort)

        return upcomingList
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return upcomingList


def lookupPopular(page=1):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}&region=US")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        search = response.json()['results']
        # initialize result list
        popularList = []
        # for each result - store their data in a new list
        for result in search:
            cover = result["poster_path"]
            # parse release date info
            # NEED TO FIX THIS -> IF THE RELEASE DATE INFO IS INACCURATE
            date_obj = datetime.strptime(result["release_date"], '%Y-%m-%d')
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            popularList.append({
                "name": result["original_title"],
                "id": result["id"],
                "release": release_year,
                "full_release": release_date,
                "rating": result["vote_average"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "type": "movie"
            })

            def sort(e):
                return e['full_release']

            popularList.sort(reverse=False, key=sort)

        return popularList
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return popularList


def lookupCast(id):
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
        castList = []
        crewList = []

        # jsonify response
        cast = response.json()['cast']
        crew = response.json()['crew']

        # Create cast list
        if cast != []:
            for i in range(len(cast)):
                picPath = cast[i]['profile_path']
                character = cast[i]['character']
                if picPath is None:
                    picPath = 'None'
                if character == '':
                    character = 'None'
                castList.append({
                    "id": cast[i]['id'],
                    "name": cast[i]['name'],
                    "picture": f'https://www.themoviedb.org/t/p/original{picPath}',
                    "character": character
                })
        # Create crew list
        for i in crew:
            if i['job'] == 'Director':
                crewList.append({
                    "name": i['name'],
                    "id": i['id']
                })
        if cast != [] and crew != []:
            # create credits object with cast and crew lists
            creditsList = {
                "cast": castList,
                "crew": crewList
            }
        elif crew == []:
            creditsList = {
                "cast": crewList,
                "crew": 'N/A'
            }
        elif cast == []:
            creditsList = {
                "cast": 'N/A',
                "crew": crewList
            }
        else:
            creditsList = {
                "cast": 'N/A',
                "crew": 'N/A'
            }
        # return
        return creditsList
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return creditsList


def lookupTvCast(id):
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/tv/{id}/credits?api_key={api_key}&language=en-US")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:

        # jsonify response
        cast = response.json()['cast']
        # Create cast list
        if cast != []:
            castList = []
            for i in range(len(cast)):
                picPath = cast[i]['profile_path']
                character = cast[i]['character']
                if picPath is None:
                    picPath = 'None'
                if character == '':
                    character = 'None'
                castList.append({
                    "id": cast[i]['id'],
                    "name": cast[i]['name'],
                    "picture": f'https://www.themoviedb.org/t/p/original{picPath}',
                    "character": character
                })

        if cast == []:
            castList = 'N/A'

        # return
        return castList
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return castList


def lookupPersonMovies(id):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/person/{id}/combined_credits?api_key={api_key}&language=en-US")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        movies = response.json()
        # initialize result list
        results = []
        search = movies['cast']
        # for each result - store their data in a new list
        for result in search:
            cover = result["poster_path"]
            if 'release_date' not in result:
                release_year = 'TBA'
                date_obj = 'TBA'
            elif result["release_date"] == '' or result["release_date"] is None:
                release_year = 'TBA'
                date_obj = 'TBA'
            else:
                # parse release date info
                date_obj = datetime.strptime(
                    result["release_date"], '%Y-%m-%d')
                release_year = date_obj.strftime('%Y')
                release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            results.append({
                "name": result["original_title"],
                "id": result["id"],
                "release": release_year,
                "full_release": date_obj,
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"],
                "type": result["media_type"]
            })

            def sort(e):
                return e['release']

            results.sort(reverse=True, key=sort)

        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results


def lookupPersonProfile(id):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/person/{id}?api_key={api_key}&language=en-US&append_to_response=images")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        movies = response.json()
        # initialize result list
        results = []
        picList = []
        profilePic = movies["profile_path"]

        if "birthday" not in movies:
            birthday = 'TBA'
            date_obj = 'TBA'
            age = 'TBA'
        elif movies["birthday"] == '' or movies["birthday"] is None:
            birthday = 'TBA'
            date_obj = 'TBA'
            age = 'TBA'
        else:
            # parse release date info
            date_obj = datetime.strptime(
                movies["birthday"], '%Y-%m-%d')
            birthday = date_obj.strftime('%B %d, %Y')
            age = round(abs(date_obj - datetime.now()).days / 365)
        for picture in movies["images"]["profiles"]:
            pic = picture["file_path"]
            filePath = f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{pic}'
            picList.append(filePath)
        # create an object and add it to our results list
        results.append({
            "name": movies["name"],
            "id": movies["id"],
            "biography": movies["biography"],
            "job": movies["known_for_department"],
            "birthday": birthday,
            "age": age,
            "profilePicture": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{profilePic}',
            "imdb": movies["imdb_id"],
            "birthLocation": movies["place_of_birth"],
            "pictures": picList
        })
        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results


def lookupPersonName(name, page=1):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/search/person?api_key={api_key}&language=en-US&query={name}&page={page}")
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
            profilePic = result["profile_path"]
            # create an object and add it to our results list
            results.append({
                "name": result["name"],
                "id": result["id"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{profilePic}',
                "popularity": result["popularity"]
            })

            def sort(e):
                return e['popularity']

            results.sort(reverse=True, key=sort)

        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results


def lookup(movie, page=1):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie}&page={page}&include_adult=false&region=US")
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
            if 'release_date' not in result:
                release_year = 'TBA'
                date_obj = 'TBA'
            elif result["release_date"] == '' or result["release_date"] is None:
                release_year = 'TBA'
                date_obj = 'TBA'
            else:
                # parse release date info
                date_obj = datetime.strptime(
                    result["release_date"], '%Y-%m-%d')
                release_year = date_obj.strftime('%Y')
                release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            results.append({
                "name": result["original_title"],
                "id": result["id"],
                "release": release_year,
                "full_release": date_obj,
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

def lookupGenre(genre, page=1):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=en-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&with_genres={genre}&page={page}")
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
            if 'release_date' not in result:
                release_year = 'TBA'
                date_obj = 'TBA'
            elif result["release_date"] == '' or result["release_date"] is None:
                release_year = 'TBA'
                date_obj = 'TBA'
            else:
                # parse release date info
                date_obj = datetime.strptime(
                    result["release_date"], '%Y-%m-%d')
                release_year = date_obj.strftime('%Y')
                release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            results.append({
                "name": result["original_title"],
                "id": result["id"],
                "release": release_year,
                "full_release": date_obj,
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


def lookupTvGenre(genre, page=1):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/discover/tv?api_key={api_key}&language=en-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&with_genres={genre}&page={page}")
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
            if 'first_air_date' not in result:
                release_year = 'TBA'
                date_obj = 'TBA'
            elif result["first_air_date"] == '' or result["first_air_date"] is None:
                release_year = 'TBA'
                date_obj = 'TBA'
            else:
                # parse release date info
                date_obj = datetime.strptime(
                    result["first_air_date"], '%Y-%m-%d')
                release_year = date_obj.strftime('%Y')
                release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            results.append({
                "name": result["original_name"],
                "id": result["id"],
                "release": release_year,
                "full_release": date_obj,
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"],
                "mediaType": "tv"
            })

            def sort(e):
                return e['release']

            results.sort(reverse=True, key=sort)

        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results

# -------------------------------------------- TODO -----------------------------------------------------------------------------


def lookupTv(title, page=1):
    # Contact API
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={title}&language=en-US&page={page}&include_adult=false")
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
            if "first_air_date" not in result:
                release_year = 'TBA'
                date_obj = 'TBA'
            elif result["first_air_date"] == '' or result["first_air_date"] is None:
                release_year = 'TBA'
                date_obj = 'TBA'
            else:
                # parse release date info
                date_obj = datetime.strptime(
                    result["first_air_date"], '%Y-%m-%d')
                release_year = date_obj.strftime('%Y')
                release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            results.append({
                "name": result["original_name"],
                "id": result["id"],
                "release": release_year,
                "full_release": result["first_air_date"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"],
                "type": "tv"
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
        backdrop = movies["backdrop_path"]
        # parse release date info
        release = lookupReleaseDate(movies['id'])
        trailer = lookupTrailer(id)
        credits = lookupCast(id)
        # THIS NEEDS WORK CLEARLY
        if movies["release_date"] == '':
            date_obj = datetime.now()
            # release_year = 'N/A'
            release_date = 'N/A'
        elif release['digital']['full'] == 'TBA' and release['theatre']['full'] == 'TBA' or not release['digital']['full'] and not release['theatre']['full']:
            date_obj = datetime.strptime(
                movies["release_date"], '%Y-%m-%d')
            # release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
        elif release['digital']['full'] == 'TBA':
            release_date = release['theatre']['full']
            date_obj = datetime.strptime(
                release['theatre']['small'], '%Y-%m-%d')
        elif release['theatre']['full'] == 'TBA':
            release_date = release['digital']['full']
            date_obj = datetime.strptime(
                release['digital']['small'], '%Y-%m-%d')
        # Added to fix bug in API where somehow the THEATRE date was later than the DIGITAL date
        elif release['theatre']['small'] > release['digital']['small']:
            release_date = release['theatre']['full']
            date_obj = datetime.strptime(
                release['theatre']['small'], '%Y-%m-%d')
        else:
            release_date = release['digital']['full']
            date_obj = datetime.strptime(
                release['digital']['small'], '%Y-%m-%d')
        released = date_obj.date() <= datetime.now().date()
        # create an object and add it to our results list
        results.append({
            "name": movies["original_title"],
            "id": movies["id"],
            "release_obj" : release,
            "release_small": date_obj.date(),
            "release_full": release_date,
            "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
            "rating": movies["vote_average"],
            "imdb": movies["imdb_id"],
            "released": released,
            "trailer": trailer,
            "overview": movies["overview"],
            "genres": movies["genres"],
            "director": credits['crew'],
            "cast": credits['cast'],
            "backdrop": backdrop
            # "backdrop": f'http://image.tmdb.org/t/p/w1920_and_h1080_multi_faces{backdrop}'
        })
        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results


def lookupTvById(id):
    try:
        # retrieve api_key
        api_key = configuration.API_KEY_STORAGE
        response = requests.get(
            f"https://api.themoviedb.org/3/tv/{id}?api_key={api_key}&language=en-US&region=CA")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        shows = response.json()
        cast = lookupTvCast(id)
        # initialize result list
        results = []
        # creators = []
        # genres = []
        # pre-set cover to be used in f string
        cover = shows["poster_path"]
        backdrop = shows["backdrop_path"]
        # parse release date info
        # THIS NEEDS WORK CLEARLY
        if shows["first_air_date"] == '' or "first_air_date" not in shows or shows["first_air_date"] == None:
            date_obj = datetime.now()
            release_year = 'N/A'
            release_date = 'N/A'
        else:
            date_obj = datetime.strptime(
                shows["first_air_date"], '%Y-%m-%d')
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
        results.append({
            "name": shows["name"],
            "id": shows["id"],
            "release_year": release_year,
            "release_full": release_date,
            "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
            "rating": shows["vote_average"],
            "status": shows["status"],
            "overview": shows["overview"],
            "genres": shows["genres"],
            "cast": cast,
            "creators": shows['created_by'],
            "episodes": shows["number_of_episodes"],
            "seasons": shows["number_of_seasons"],
            "backdrop": f'http://image.tmdb.org/t/p/w1920_and_h1080_multi_faces{backdrop}'
        })
        return results
    except (KeyError, TypeError, ValueError):
        return None
    finally:
        return results


# if __name__ == "__main__":
#     print(lookupTrailer('641662'))
#     print(lookupReleaseDate('464052'))
