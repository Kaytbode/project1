import os

from flask import Flask, session, render_template, request, redirect, url_for, flash
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
session = scoped_session(sessionmaker(bind=engine))
db = session()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signIn", methods=["GET", "POST"])
def signIn():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPw = request.form.get('confirmPassword')

        if password == confirmPw:
            db.execute("INSERT INTO users(username, passwd) VALUES(:username, :passwd)", 
                {'username': username, 'passwd': password})
            db.commit()
            message = 'You successfully registered!'
            return render_template('signIn.html', message=message)
        else:
            flash('The passwords you entered do not match!')
            return redirect(url_for('index'))

    return render_template('signIn.html', message='Have you registered ?')

@app.route("/Books", methods=["POST"])
def books():
    if 'signIn' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
       
        user = db.execute("SELECT * FROM users WHERE username=:username",
                {"username": username}).fetchone()
        
        db.commit()

        if not user:
            flash('User not registered')
            return redirect(url_for('signIn'))

        if user.passwd == password:
            return render_template('books.html')
        else:
            flash('Password is incorrect!')
            return redirect(url_for('signIn'))
    
    elif 'searchBook' in request.form:
        book = request.form.get('search')
        book = ' '.join(chr.capitalize() for chr in book.split())
    
        books = db.execute("SELECT * FROM books WHERE isbn like :book OR title like :book OR author like :book",
            {'book' : '%'+book+'%'}).fetchall()
        db.commit()

        if not books:
            flash('Book not found')
            return render_template('books.html')
        else:
            return render_template('books.html', books= books)