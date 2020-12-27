import os
import configuration
import re

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import flash, g, redirect, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from api import lookup, lookupById
from utilities import login_required

# define our flask app
app = Flask(__name__)

# setting up config
app.config['SECRET_KEY']=configuration.SECRET_KEY_STORAGE

# used to switch DB
ENV = 'launch'
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI']=conifguration.DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
# gets rid of annoying error message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# our database models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Follows(db.Model):
    __tablename__ = 'follows'
    follow_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    movie_title = db.Column(db.String)
    movie_date= db.Column(db.Text())
    
    def __init__(self, user_id, movie_id, movie_title, movie_date):
        self.user_id = user_id
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.movie_date = movie_date

# main page route
@app.route('/', methods=('GET', 'POST'))
def index():
    # acquire the movie title from form and pass it to the results page
    if request.method == 'POST':
        query = request.form['movie_title']
        # parse input to make sure its not empty and that the search will return some results
        if query == '':
            error = 'Please provide a movie title'
        # parse input to make sure it has some results
        elif lookup(query) == []:
            error = 'Please refine your search query to be more specific'
        # if valid and results are found - redirect to results page - passing the query
        else: 
            return redirect(url_for('results', query=query)) 
        # flash error
        flash(error)
    # get request will display index
    return render_template('dashboard/index.html')

# results route - takes one argument which is the query string
@app.route('/results/<query>', methods=('GET', 'POST'))
def results(query):
    # use our api to get results based on query string
    searchQuery = lookup(query)
    # render template with results
    if request.method == 'GET':
        return render_template('search/results.html', results=searchQuery)
    # if user clicks the follow button
    elif request.method == 'POST':
        # get the movie id from the form and look it up in our api
        id = request.form['movie_id']
        movie = lookupById(id)[0]
        # set error to none
        error = None
        # check to make sure user is not already following
        if db.session.query(Follows).filter(Follows.user_id == session['user_id'], Follows.movie_id == movie['id']).count() > 0:
            # set error message appropriately
            error = 'You are already following {}!'.format(movie['name'])
        # if not following then insert the follow into the database
        else:
            insert_follow = Follows(session['user_id'], movie['id'], movie['name'], movie['release_date'])
            db.session.add(insert_follow)
            db.session.commit()
            # flask success message and re-render template
            flash('Now following {}!'.format(movie['name']))
            return render_template('search/results.html', results=searchQuery)
        # flash error message
        flash(error)

# details route to show movie info and imdb link / takes one arguement (id of the movie)
@app.route('/<int:id>/details', methods=('GET', 'POST'))
def details(id):
    # if get - then get api information and pass that to the template
    if request.method == 'GET':
        movie = lookupById(id)
        return render_template('search/details.html', details=movie)
    # else if they click the follow button
    elif request.method == 'POST':
        movie = lookupById(id)[0]
        error = None
        # check to make sure user is not already following
        if db.session.query(Follows).filter(Follows.user_id == g.user.id, Follows.movie_id == movie['id']).count() > 0:
            error = 'You are already following {}!'.format(movie['name'])
        else:
            # if not following then insert the follow into the database
            insert_follow = Follows(g.user.id, movie['id'], movie['name'], movie['release_date'])
            db.session.add(insert_follow)
            db.session.commit()
            # success message and reload new follows page
            flash('Now following {}!'.format(movie['name']))
            return redirect(url_for('follows'))
        # flash any error message
        flash(error)

# register route
@app.route('/auth/register', methods=('GET', 'POST'))
def register():
    # on post - retrieve info from our form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        # pre-set error to None
        error = None

        # init regex
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-_])[A-Za-z\d@$!#%*?&-_]{6,20}$"
        # Compile Regex
        pat = re.compile(reg)
        # Search Regex
        mat = re.search(pat, password)

        # parse input
        if not username:
            error = 'You must provide a username'
        elif not password:
            error = 'You must provide a password'
        # make sure username doesn't already exist
        if db.session.query(User).filter(User.username == username).count() > 0:
            error = 'User {} is already registered'.format(username)
        # make sure passwords match
        elif password != confirm:
            error = 'Passwords must match'
        elif not mat:
            error = 'Password must contain (one number / one uppercase / one lowercase / one special symbol (@$!%*#?&-_) / be between 6-20 characters'
        # if no errors then insert user into database
        if error is None:
            insert_user = User(username, generate_password_hash(password))
            db.session.add(insert_user)
            db.session.commit()
            # flash success message
            flash('Now Registered As: {}! Please Login.'.format(username))
            return redirect(url_for('login'))
        # flash any errors
        flash(error)
    # if get then render tamplate  
    return render_template('auth/register.html')

# login route
@app.route('/auth/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        # on post - retrieve info from our form
        username = request.form['username']
        password = request.form['password']
        error = None

        # check for user in database and pull their info if it exists
        user = User.query.filter_by(username = username).first()
        # if valid input and user exists - set our session data
        if user and check_password_hash(user.password, password) == True:
            session.clear()
            session['user_id'] = user.id
            # redirect to home page
            return redirect(url_for('index'))
        # parse for errors and set error message accordingly
        elif not user or user is None:
            error = 'User not found'
        elif not username or not password:
            error = 'You must fill in both fields'
        else:
            error = 'Invalid password'
        # flash error if there is one
        flash(error)
    # get request renders template
    return render_template('auth/login.html')

# follows route to display users followed movies
@app.route('/user/follows', methods=('GET', 'POST'))
@login_required
def follows():
    # couldn't get login_required to work - so using this for now
    if request.method == 'GET':
        follows = db.session.query(Follows.movie_id).filter(Follows.user_id == session['user_id']).all()
        followList = []

        for i in range(len(follows)):
            movie_id = lookupById(follows[i].movie_id)[0]
            followList.append({
                "name": movie_id["name"],
                "id": movie_id["id"],
                "release": movie_id["release"],
                "cover" : movie_id["cover"],
                "rating": movie_id["rating"],
                "released": movie_id["released"]
            })
        
        return render_template('user/follows.html', follows = followList)
    elif request.method == 'POST':
        id = request.form['movie_id']
        user = g.user.id

        delete_this = db.session.query(Follows).filter(Follows.movie_id == id, Follows.user_id==user).one()
        
        db.session.delete(delete_this)
        db.session.commit()
        # print(delete_this[0].movie_title)


        follows = db.session.query(Follows.movie_id).filter(Follows.user_id == session['user_id']).all()

        followList = []

        for i in range(len(follows)):
            movie_id = lookupById(follows[i].movie_id)[0]
            followList.append({
                "name": movie_id["name"],
                "id": movie_id["id"],
                "release": movie_id["release"],
                "cover" : movie_id["cover"],
                "rating": movie_id["rating"],
                "released": movie_id["released"]
            })
        
        return render_template('user/follows.html', follows = followList)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))

# logout route
@app.route('/logout')
def logout():
    g.user = None
    session.clear()
    return redirect(url_for('index'))

@app.before_first_request
def init_request():
    db.create_all()

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        user = User.query.filter_by(id=user_id).all()
        g.user=user[0]

# if __name__ == '__main__':
#     app.run()