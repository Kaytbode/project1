import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
session_db = scoped_session(sessionmaker(bind=engine))
db = session_db()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signIn", methods=["GET", "POST"])
def signIn():

    """ User Registeration """

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPw = request.form.get('confirmPassword')

        # if password inputs match, insert into database
        if password == confirmPw:
            try:
                db.execute("INSERT INTO users(username, passwd) VALUES(:username, :passwd)", 
                    {'username': username, 'passwd': password})
                db.commit()
                message = 'You successfully registered!'
                return render_template('signIn.html', message=message)
            except:
                flash('Cannot connect to database. Please try again')
                return redirect(url_for('index'))
        else:
            flash('The passwords you entered do not match!')
            return redirect(url_for('index'))

    return render_template('signIn.html', message='Have you registered ?')

@app.route("/SignOut")
def signOut():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/Books", methods=["POST"])
def books():

    """ Display Book search results """
    
    if 'signIn' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
       
        try:
            user = db.execute("SELECT * FROM users WHERE username=:username",
                    {"username": username}).fetchone()
            db.commit()
        except:
            flash('You are not connected.')
            return redirect(url_for('signIn'))

        #Check if user is registered
        if not user:
            flash('User not registered')
            return redirect(url_for('signIn'))

        #password check
        if user.passwd == password:
            session['username'] = username
            return render_template('books.html', username=username)
        else:
            flash('Password is incorrect!')
            return redirect(url_for('signIn'))
    
    elif 'searchBook' in request.form:
        book = request.form.get('search')
        book = ' '.join(chr.capitalize() for chr in book.split())
    
        try:
            books = db.execute("SELECT * FROM books WHERE isbn like :book OR title like :book OR author like :book",
                {'book' : f'%{book}%'}).fetchall()
            db.commit()
        except:
            flash('Not connected to database')
            return render_template('books.html')
        
        # did the request return any results?
        if not books:
            flash('Book not found')
            return render_template('books.html')
        else:
            return render_template('books.html', books= books, username=session['username'])

@app.route("/Books/<isbn>", methods=["GET", "POST"])
def book(isbn):

    """ Display book details """

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # check if user has submitted a review
        try:
            username = db.execute("SELECT username FROM reviews WHERE username=:username", {'username': session['username']})
        except:
            flash('Not connected to database')
        
        if not username:
            try:
                db.execute("INSERT INTO reviews(username, book, comment, rating) VALUES(:username, :book, :comment, :rating)",
                    {'username': session['username'], 'book': isbn, 'comment': comment, 'rating': rating})
                db.commit()
            except:
                flash('Cannot post review to database')

        else:
            flash('You can only post one review per book')
        
    # if user tries to access the url without registering
    if not session['username']:
        flash('You are not a registered User')
        return redirect(url_for('index'))
    
    try:
        book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()
        db.commit()

        reviews = db.execute("SELECT * FROM reviews WHERE book=:book", {'book':isbn}).fetchall()
        db.commit()
    except:
        flash('Not connected to database')
        redirect(url_for('books'))
    
    # Fetch data from Goodreads
    try:
        api_key = os.getenv("GOODREADS_KEY") #'4AcUrYrpY3jO72H6fnP8MQ'
        api_url = f'https://www.goodreads.com/book/review_counts.json?isbns={isbn}&key={api_key}'
        req = requests.get(api_url)
        good_reads = req.json()['books'][0]
    except:
        flash('Could not retrieve ratings from Goodreads')

    return render_template('book.html', book= book, ratings = good_reads['work_ratings_count'], avg_rating=good_reads['average_rating'],
    reviews=reviews, username=session['username'])

@app.route("/api/<isbn>")
def api(isbn):

    """ API access """

    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()
    db.commit()

    if not book:
        return render_template('page404.html', message=404)
    else:
        count = db.execute("SELECT COUNT(book) FROM reviews WHERE book=:book", {'book':isbn}).fetchall()
        db.commit()
        score = db.execute("SELECT AVG(rating) FROM reviews WHERE book=:book", {'book':isbn}).fetchall()
        db.commit()

    avg_score = float(score[0][0])
    data = {
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'isbn': book.isbn,
        'review_count': count[0][0],
        'average_score': avg_score
        }

    return jsonify(data)

