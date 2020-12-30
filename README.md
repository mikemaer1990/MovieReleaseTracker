# Movie Release Date Tracker
## Basic App To Follow Upcoming Movies
###### My CS50x Final Project
[GitHub](https://github.com/mikemaer1990/moviereleasetracker)
This site was built using [Python](https://www.python.org/) & [Flask](https://flask.palletsprojects.com/en/1.1.x/)

Basic way to keep track of upcoming movies - just search for the movie you would like to follow and follow it.

You will receive an email on the day any of your followed movies are released.

I did have all of my modules separated properly, and was using an SQLite database. Unfortunately, I realized that sqlite is useless with Heroku so I started the process of switching over to PostgreSQL with SQLAlchemy. I could not successfully get it working without most of my app all inside app.py. I will figure this out in the future. If anyone by chance sees this and has any advice, let me know!

## TODOS
1. Add TV Shows Option
2. Enable Multiple Results Pages
3. Upcoming Releases Page
4. More Data on Details Page
5. Search bar in the navbar! --- PRIORITY
6. Option to have emails at different times - week before, etc.
