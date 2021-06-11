import requests
import configuration
import math
import re
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

api_key = configuration.API_KEY_STORAGE

def grabPages(count, index, address):
    results = []
    pageCount = requests.get(
        f"{address}").json()["total_pages"]
    for i in range(index, index + count, 1):
        if i > pageCount:
            break
        try:
            response = requests.get(
                f"{address}&page={i}")
            response.raise_for_status()
        except requests.RequestException:
            break
            # Parse response
        try:
            # jsonify response
            search = response.json()['results']
            results += search
        except Exception as e:
            print(e)
            break
    return results

def multiSearch(query, page=1, adult=False):
    # Contact API
    try:
        address = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&language=en-US&include_adult={adult}&query={query}&region=US"
        page_chunk = 2
        if page == 1:
            page = page
        else:
            page = (page * page_chunk) + 1 - page_chunk
        search = grabPages(page_chunk, page, address)
        # initialize result list
        results = []
        # for each result - store their data in our results list
        for result in search:
            # Set cover to none to prevent errors
            cover = None
            # Set rating default to '-'
            rating = 'N/A'
            # Don't include Bollywood films --- sorry!
            if 'original_language' in result and result['original_language'] == 'hi':
                continue
            # For movies...
            if result['media_type'] == 'movie':
                # If no release date info
                if 'release_date' not in result or result['release_date'] == '':
                    name = result['title']
                    date_obj = 'N/A'
                    release_year = 'N/A'
                else:
                    # parse release date info
                    date_obj = datetime.strptime(
                    result["release_date"], '%Y-%m-%d')
                    name = result['title']
                    release_year = date_obj.strftime('%Y')
                    cover = result["poster_path"]
                    rating = result['vote_average']
            # For TV...
            elif result['media_type'] == 'tv':
                # If no release date info
                if 'first_air_date' not in result or result['first_air_date'] == '':
                    name = result['original_name']
                    date_obj = 'N/A'
                    release_year = 'N/A'
                else:
                    date_obj = datetime.strptime(
                    result["first_air_date"], '%Y-%m-%d')
                    name = result['original_name']
                    release_year = date_obj.strftime('%Y')
                    cover = result["poster_path"]
                    rating = result['vote_average']
            # For People...
            elif result['media_type'] == 'person':
                date_obj = 'N/A'
                release_year = result['known_for_department']
                name = result['name']
                cover = result["profile_path"]
                rating = result['popularity']
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
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        return results

def convert_release_type(number):
    if number == 1:
        return 'Premiere'
    elif number == 2:
        return 'Theatre (Limited)'
    elif number == 3:
        return 'Theatre'
    elif number == 4:
        return 'Digital'
    elif number == 5:
        return 'DVD'
    elif number == 6:
        return 'TV'

def lookupReleaseDatee(id, country_code='US'):
    release_list = []
    try:
        # retrieve api_key
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}/release_dates?&api_key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        response = response.json()['results']
        try:
            for country in response:
                if country['iso_3166_1'] == country_code:
                    release_list_temp = []
                    for release_type in country['release_dates']:
                        date_obj = datetime.strptime(release_type['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        date_small = date_obj.strftime('%Y-%m-%d')
                        date_full = date_obj.strftime('%B %d, %Y')
                        release_list_temp.append({
                            "country": country['iso_3166_1'],
                            "type": convert_release_type(release_type['type']),
                            "full": date_full,
                            "small": date_small
                        })
            def sort(e):
                return e['small']
            release_list_temp.sort(reverse=False, key=sort)
            return release_list_temp
        except:
            for country in response:
                release_list_temp = []
                for release_type in country['release_dates']:
                    date_obj = datetime.strptime(release_type['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    date_small = date_obj.strftime('%Y-%m-%d')
                    date_full = date_obj.strftime('%B %d, %Y')
                    release_list_temp.append(
                        {
                            "country": country['iso_3166_1'],
                            "type": convert_release_type(release_type['type']),
                            "full": date_full,
                            "small": date_small
                        }
                    )
                def sort(e):
                    return e['small']
                release_list_temp.sort(reverse=False, key=sort)
                release_list.append(release_list_temp)
        return release_list
    except Exception as e:
        print(e)
        return None

def lookupReleaseDate(id):
    release_obj = None
    digital = None
    theatre = None
    tvDate = None
    premiere = None
    try:
        # retrieve api_key
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
                    if y['type'] == 1:
                        premiere = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    # Digital Release Object and skip any digital release with festival in the notes due to coronavirus
                    elif y['type'] == 4 and not 'Festival' in y['note']:
                        digital = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        digital_full = digital.strftime('%B %d, %Y')
                        digital_small = digital.strftime('%Y-%m-%d')
                    # Theatrical Release Object
                    elif y['type'] == 3:
                        theatre = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        theatre_full = theatre.strftime('%B %d, %Y')
                        theatre_small = theatre.strftime('%Y-%m-%d')
                    # Hard copy DVD
                    # REMOVED ---- and y['note'] == 'DVD' here
                    elif y['type'] == 5 and digital is None:
                        digital = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        digital_full = digital.strftime('%B %d, %Y')
                        digital_small = digital.strftime('%Y-%m-%d')
                    # TV Date For Old Movies
                    elif y['type'] == 6:
                        tvDate = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    elif y['type'] == 5 and not tvDate and y['note'] == 'DVD':
                        tvDate = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    # Theatrical (Limited) For rare cases where movie release is not accurate due to Coronavirus
                    elif y['type'] == 2 and not tvDate:
                        tvDate = datetime.strptime(
                            y['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # TESTING for when no accurate info availabe for US
        if digital is None:
            for country in movies:
                if country['iso_3166_1'] != 'US':
                    for x in country['release_dates']:
                        if x['type'] == 5:
                            # if theatre is not None:
                            #     test = datetime.strptime(x['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                            #     if (test - theatre).days > 300:
                            #         continue
                            digital = datetime.strptime(
                                x['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                            digital_full = digital.strftime('%B %d, %Y')
                            digital_small = digital.strftime('%Y-%m-%d')
        if digital is None and theatre is None and tvDate is None:
            for country in movies:
                for x in country['release_dates']:
                    if x['type'] == 4:
                        digital = datetime.strptime(
                            x['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        digital_full = digital.strftime('%B %d, %Y')
                        digital_small = digital.strftime('%Y-%m-%d')
                    elif x['type'] == 3:
                        theatre = datetime.strptime(
                            x['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        theatre_full = theatre.strftime('%B %d, %Y')
                        theatre_small = theatre.strftime('%Y-%m-%d')
                    elif x['type'] == 1 and digital == None and theatre == None:
                        premiere = datetime.strptime(
                            x['release_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if theatre is None and digital is None:
            if tvDate is None and premiere is None:
                digital_full = 'TBA'
                digital_small = 'TBA'
                theatre_full = 'TBA'
                theatre_small = 'TBA'
            elif premiere is None :
                digital = tvDate
                digital_full = digital.strftime('%B %d, %Y')
                digital_small = digital.strftime('%Y-%m-%d')
            # TEMPORARY FIX FOR PREMIRE
            elif tvDate is None:
                theatre = premiere
                theatre_full = theatre.strftime('%B %d, %Y')
                theatre_small = theatre.strftime('%Y-%m-%d')
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
    except Exception as e:
        print(e)
        return None
    finally:
        return release_obj

# Function to get the youtube trailer link if available
def lookupTrailer(id):
    trailer_url = None
    try:
        # retrieve api_key
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
    except Exception as e:
        print(e)
        return None
    finally:
        return trailer_url

def lookupRelatedMovies(id):
    try:
        # retrieve api_key
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}/similar?api_key={api_key}&language=en-US&page=1")
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
    except Exception as e:
        print(e)
        return None
    finally:
        return relatedList


def lookupRelatedTv(id):
    try:
        # retrieve api_key
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
                "name": result["name"] or result["original_name"],
                "id": result["id"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "mediaType": "tv",
                "popularity": result["popularity"]
            })

        return relatedList
    except Exception as e:
        print(e)
        return None
    finally:
        return relatedList

def lookupUpcoming(page=1, sort='popularity.desc'):
    # Create date values for a 6 month window to show releases from
    three_months_ahead = date.today() + relativedelta(months=+3)
    today = date.today()
    page_chunk = 2
    if page == 1:
        page = page
    else:
        page = (page * page_chunk) + 1 - page_chunk
    
    address = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=en-US&sort_by={sort}&include_adult=false&include_video=false&page={page}&primary_release_date.gte={today}&primary_release_date.lte={three_months_ahead}"
    try:
        # Jsonify response
        search = grabPages(page_chunk, page, address)
        # Initialize result list
        results = []

        # For each result - store their data in a new list
        for result in search:
            # Get the cover image
            cover = result["poster_path"]
            # In rare cases where the list includes already released movies
            if str(result['release_date']) < str(today):
                # Check for an updated release date
                release_date_obj = lookupReleaseDate(result['id'])
                if release_date_obj['digital']['small'] != 'TBA':
                    date_obj = release_date_obj['digital']['small']
                    release_date = release_date_obj['digital']['full']
                elif release_date_obj['theatre']['small'] != 'TBA' and release_date_obj['digital']['small'] == 'TBA':
                    date_obj = release_date_obj['theatre']['small']
                    release_date = release_date_obj['theatre']['full']
            # If no release date available
            elif 'release_date' not in result:
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
            # If the release date is still below the current date - skip this movie
            if str(date_obj) < str(today):
                continue
            # create an object and add it to our results list
            results.append({
                "name": result["title"],
                "original_name": result["original_title"],
                "id": result["id"],
                "release": release_year or 'N/A',
                "full_release": release_date,
                "date_obj": date_obj,
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"]
            })
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        return results

def lookupPopular(page=1):
    try:
        address = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&region=US"
        page_chunk = 2
        if page == 1:
            page = page
        else:
            page = (page * page_chunk) + 1 - page_chunk
        search = grabPages(page_chunk, page, address)
        # initialize result list
        popularList = []
        # for each result - store their data in a new list
        for result in search:
            cover = result["poster_path"]
            # parse release date info
            date_obj = datetime.strptime(result["release_date"], '%Y-%m-%d')
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            popularList.append({
                "name": result["title"],
                "id": result["id"],
                "release": release_year,
                "full_release": release_date,
                "date_obj": date_obj,
                "rating": result["vote_average"],
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "type": "movie",
                "popularity": result["popularity"]
            })
    except Exception as e:
        print(e)
        return None
    finally:
        return popularList

def lookupRecent(page=1, sort='popularity.desc'):
    # Create date values for a 6 month window to show releases from
    one_month_behind = date.today() + relativedelta(months=-1)
    today = date.today()
    page_chunk = 2
    if page == 1:
        page = page
    else:
        page = (page * page_chunk) + 1 - page_chunk
    
    address = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=en-US&sort_by={sort}&include_adult=false&include_video=false&page={page}&primary_release_date.lte={today}&primary_release_date.gte={one_month_behind}"
    try:
        # Jsonify response
        search = grabPages(page_chunk, page, address)
        # Initialize result list
        results = []
        # For each result - store their data in a new list
        for result in search:
            # Get the cover image
            cover = result["poster_path"]
            # In rare cases where the list includes already released movies
            # if str(result['release_date']) > str(today):
            #     # Check for an updated release date
            #     release_date_obj = lookupReleaseDate(result['id'])
            #     if release_date_obj['digital']['small'] != 'TBA':
            #         date_obj = release_date_obj['digital']['small']
            #         release_date = release_date_obj['digital']['full']
            #     elif release_date_obj['theatre']['small'] != 'TBA' and release_date_obj['digital']['small'] == 'TBA':
            #         date_obj = release_date_obj['theatre']['small']
            #         release_date = release_date_obj['theatre']['full']
            # # If no release date available
            # elif 'release_date' not in result:
            #     release_year = 'TBA'
            #     date_obj = 'TBA'
            # elif result["release_date"] == '' or result["release_date"] is None:
            #     release_year = 'TBA'
            #     date_obj = 'TBA'
            # else:
            # parse release date info
            date_obj = datetime.strptime(
                result["release_date"], '%Y-%m-%d')
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
            # If the release date is still below the current date - skip this movie
            # if str(date_obj) > str(today):
            #     continue
            # create an object and add it to our results list
            results.append({
                "name": result["title"],
                "original_name": result["original_title"],
                "id": result["id"],
                "release": release_year or 'N/A',
                "full_release": release_date,
                "date_obj": date_obj,
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"]
            })
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        return results

def lookupCast(id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}/credits?api_key={api_key}&language=en-US")
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        # Initialize cast and crew lists
        castList = []
        crewList = []

        # jsonify response
        cast = response.json()['cast']
        crew = response.json()['crew']

        # Sort them by popularity
        def sort(e):
            return e['popularity']
        cast.sort(reverse=True, key=sort)
        crew.sort(reverse=True, key=sort)
        
        # Create cast list
        if cast != []:
            for i in range(len(cast)):
                # Get picture path and character name
                picPath = cast[i]['profile_path'] or 'None'
                character = cast[i]['character'] or 'None'
                # if picPath is None:
                #     picPath = 'None'
                # if character == '':
                #     character = 'None'
                # Push each cast member object to cast list
                castList.append({
                    "id": cast[i]['id'],
                    "name": cast[i]['name'],
                    "picture": f'https://www.themoviedb.org/t/p/original{picPath}',
                    "character": character
                })
        # Create crew list (director(s))
        for i in crew:
            if i['job'] == 'Director':
                crewList.append({
                    "name": i['name'],
                    "id": i['id']
                })
        # If both lists are not empty
        if cast != [] and crew != []:
            # create credits object with cast and crew lists
            creditsList = {
                "cast": castList,
                "crew": crewList
            }
        # elif crew == []:
        #     creditsList = {
        #         "cast": crewList,
        #         "crew": 'N/A'
        #     }
        # elif cast == []:
        #     creditsList = {
        #         "cast": 'N/A',
        #         "crew": crewList
        #     }
        # If either or both lists are empty
        else:
            creditsList = {
                "cast": castList or 'N/A',
                "crew": crewList or 'N/A'
            }
        # Return our credits object
        return creditsList
    except Exception as e:
        print(e)
        return None
    finally:
        return creditsList


def lookupTvCast(id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/tv/{id}/credits?api_key={api_key}&language=en-US")
        response.raise_for_status()
    except requests.RequestException:
        return None
        # Parse response
    try:
        # jsonify response
        crew = response.json()['crew']
        cast = response.json()['cast']

        # Sort them by popularity
        def sort(e):
            return e['popularity']
        cast.sort(reverse=True, key=sort)
        crew.sort(reverse=True, key=sort)

        # Create cast list
        if cast != []:
            castList = []
            for i in range(len(cast)):
                # Get picture path and character name
                picPath = cast[i]['profile_path'] or 'None'
                character = cast[i]['character'] or 'None'
                # if picPath is None:
                #     picPath = 'None'
                # if character == '':
                #     character = 'None' 
                # Append each person to our list
                castList.append({
                    "id": cast[i]['id'],
                    "name": cast[i]['name'],
                    "picture": f'https://www.themoviedb.org/t/p/original{picPath}',
                    "character": character
                })
        # If crew exists
        # if crew != []:
        #     crewList = []
        #     # Push each director into the list
        #     for i in crew:
        #         if i['job'] == 'Director':
        #             crewList.append({
        #                 "name": i['name'],
        #                 "id": i['id']
        #         })
        # # 
        # If castList is empty
        if cast == []:
            castList = 'N/A'
        # Return list of cast members
        return castList
    except Exception as e:
        print(e)
        return None
    finally:
        return castList


def lookupPersonMovies(id):
    # Contact API
    try:
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
    except Exception as e:
        print(e)
        return None
    finally:
        return results

def lookupPersonProfile(id):
    # Contact API
    try:
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
        bio = None
        deathday = None
        profilePic = movies["profile_path"]
        if "birthday" not in movies:
            birthday = 'N/A'
            date_obj = 'N/A'
            age = 'N/A'
        elif movies["birthday"] == '' or movies["birthday"] is None:
            birthday = 'N/A'
            date_obj = 'N/A'
            age = 'N/A'
        else:
            # parse release date info
            date_obj = datetime.strptime(
                movies["birthday"], '%Y-%m-%d')
            birthday = date_obj.strftime('%B %d, %Y')
            if movies['deathday'] == None:
                age = round(abs(date_obj - datetime.now()).days / 365)
                deathday = None
            else:
                death_date_obj = datetime.strptime(
                    movies["deathday"], '%Y-%m-%d')
                age = math.floor(abs(date_obj - death_date_obj).days / 365)
                deathday = death_date_obj.strftime('%B %d, %Y')
        for picture in movies["images"]["profiles"]:
            pic = picture["file_path"]
            filePath = f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{pic}'
            picList.append(filePath)
        # Crop unnecessary Wikipedia mention
        if movies['biography'] and movies['biography'] != '' and movies['biography'] is not None:
            bio = movies['biography'].replace('From Wikipedia, the free encyclopedia\n\n', '')
            reg = "(Description)(.*)\."
            pat = re.compile(reg)
            bio = re.sub(pat, '', bio)
        # create an object and add it to our results list
        results.append({
            "name": movies["name"],
            "id": movies["id"],
            "biography": bio,
            "job": movies["known_for_department"],
            "birthday": birthday,
            "deathday": deathday or None,
            "age": age,
            "profilePicture": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{profilePic}',
            "imdb": movies["imdb_id"],
            "birthLocation": movies["place_of_birth"] or 'N/A',
            "pictures": picList
        })
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        return results

def lookupGenre(mediaType, genre, page=1, sort='popularity.desc'):
    # Create date values for a 6 month window to show releases from
    address = f"https://api.themoviedb.org/3/discover/{mediaType}?api_key={api_key}&language=en-US&sort_by={sort}&include_adult=false&include_video=false&with_genres={genre}"
    page_chunk = 2
    if page == 1:
        pass
    else:
        page = (page * page_chunk) + 1 - page_chunk
    search = grabPages(page_chunk, page, address)
    # Contact API
    try:
        # initialize result list
        results = []
        # for each result - store their data in a new list
        for result in search:
            cover = result["poster_path"]
            if mediaType == 'movie':
                name = result["title"]
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
            elif mediaType == 'tv':
                name= result['name']
                # If no release date info
                if 'first_air_date' not in result or result['first_air_date'] == '':
                    date_obj = 'N/A'
                    release_year = 'N/A'
                else:
                    date_obj = datetime.strptime(
                        result["first_air_date"], '%Y-%m-%d')
                    release_year = date_obj.strftime('%Y')
                    release_date = date_obj.strftime('%B %d, %Y')
            # create an object and add it to our results list
            results.append({
                "name": name,
                "id": result["id"],
                "release": release_year,
                "release_date": release_date,
                "full_release": date_obj,
                "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
                "rating": result["vote_average"]
            })
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        return results


def lookupTvGenre(genre, page=1):
    # Contact API
    try:
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
    except Exception as e:
        print(e)
        return None
    finally:
        return results

# function to lookup movies by id
def lookupById(id):
    try:
        # retrieve api_key
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
            "name": movies["title"],
            "original_name": movies['original_title'],
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
        })
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        return results


def lookupTvById(id):
    try:
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
                shows['first_air_date'], '%Y-%m-%d')
            release_year = date_obj.strftime('%Y')
            release_date = date_obj.strftime('%B %d, %Y')
        if shows['status'] == 'Ended' or shows['status'] == 'Canceled':
            end_date_obj = datetime.strptime(
                shows['last_air_date'], '%Y-%m-%d')
            ended_date = end_date_obj.strftime('%B %d, %Y')
        else:
            ended_date = None
        # create an object and add it to our results list
        results.append({
            "name": shows["name"],
            "id": shows["id"],
            "release_year": release_year,
            "release_full": release_date,
            "ended_date" : ended_date or 'N/A',
            "cover": f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{cover}',
            "rating": shows["vote_average"],
            "status": shows["status"],
            "overview": shows["overview"],
            "genres": shows["genres"],
            "cast": cast,
            "creator": shows['created_by'],
            "episodes": shows["number_of_episodes"],
            "seasons": shows["number_of_seasons"],
            "backdrop": f'http://image.tmdb.org/t/p/w1920_and_h1080_multi_faces{backdrop}'
        })
        return results
    except Exception as e:
        print(e)
        return None
    finally:
        return results

# if __name__ == "__main__":
#     print(lookupTrailer('641662'))
#     print(lookupReleaseDate('464052'))
