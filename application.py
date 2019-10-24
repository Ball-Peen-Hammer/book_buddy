import os
import requests
import json

from flask import Flask, url_for, render_template, redirect, request, session, flash, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import *
from models import *
from config import *


app = Flask(__name__)
csrf = CSRFProtect(app)

app.config.from_object('config.Config')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)

#Configure flask login.
login = LoginManager(app)
login.init_app(app)

book_id = []

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/books", methods=['GET', 'POST'])
@login_required
def books():
    form = SearchForm()
    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        author = request.form["author"]
        com_form = request.form
        if form.validate_on_submit:
            if title == "" and author == "":
               books = Library.query.filter(Library.isbn.ilike("%" + request.form["isbn"] + "%")).limit(10)
               return render_template('books.html',form=form, books=books)
            elif isbn == "" and author == "":
               books = Library.query.filter(Library.title.ilike("%" + request.form["title"] + "%")).limit(10)
               return render_template('books.html',form=form, books=books)
            elif isbn == "" and title == "":
               books = Library.query.filter(Library.author.ilike("%" + request.form["author"] + "%")).limit(10)
               return render_template('books.html',form=form, books=books)                          
            
    return render_template("books.html", form=form)


@app.route("/")
def index():
   

    
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    login_form = LoginForm()
    form = SearchForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        flash('Logged in successfully.')
        return redirect(url_for('books'))

    
    return render_template("login.html", form=login_form)

@app.route("/register", methods=["GET","POST"])
def register():
    """Register"""
    reg_form = RegistrationForm()
    if request.method == 'POST':
        if reg_form.validate_on_submit():
            username = reg_form.username.data
            password = (reg_form.password.data)
            hashed_pswd = pbkdf2_sha256.hash(password)
            

            # Add user to database
            user = User(username=username, password=hashed_pswd)
            db.session.add(user)
            db.session.commit()

            flash('Registered succesfully. Please login.')
            return redirect(url_for('login'))


  

    return render_template("register.html", form=reg_form)

@app.route("/error", methods=["GET", "POST"])
def error():

    return "oops"
    

@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash('You have logged out successfully bye for now' )
    return redirect(url_for("index"))
   
@app.route("/search_results", methods=["GET","POST"])
@login_required
def search_results():
    form = ReviewForm()
    current_user = session["user_id"]
    session['book_id'] = request.form.get("book_id")
    books = Library.query.filter_by(id=session['book_id']).first()
    key = os.getenv("API_KEY")
    isbns = books.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbns, "key": key})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    rtngs_count = data["books"][0]['work_ratings_count']
    average = data["books"][0]['average_rating']
    user_reviews = db.session.query(UserReviews).join(User).filter(UserReviews.book_id == session["book_id"]).limit(5)
    row = UserReviews.query.filter(and_(UserReviews.user_id == current_user, UserReviews.book_id == session['book_id'])).count()
    if row >= 1:
        flash("you have already reviewed this book")
        return redirect(url_for('books'))

    return render_template("search_results.html",form=form, books=books, user_reviews=user_reviews, rtngs_count=rtngs_count, average=average)

@app.route("/book_review/", methods=["GET", "POST"])
@login_required
def book_review():
    book = Library.query.filter_by(id=session['book_id']).first()
    score = request.form.get("score")
    review = request.form.get("user_review")
    book_review = UserReviews(book_id=session['book_id'], user_id=current_user.get_id(), user_score=score, user_review=review)
        
    db.session.add(book_review)
    db.session.commit()
    return render_template("book_review.html", score=score, review=review, book=book)

@app.route("/user/<user_id>", methods=["GET", "POST"])
def user(user_id):
    form = SearchForm()
    user = User.query.get(user_id)
    user_reviews = UserReviews.query.filter_by(user_id=user_id).all()
    
        
    return render_template("user.html", user=user, user_reviews=user_reviews, form=form)
   
@app.route("/api/<isbn>")
def api(isbn):
    book = Library.query.filter_by(isbn=isbn).first()
    key = os.getenv("API_KEY")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbn, "key": key})
    if res.status_code != 200:
        return jsonify({"error": "Invalid ISBN or book not in database"}), 422
    data = res.json()
    reviews_count = data["books"][0]['reviews_count']
    average = data["books"][0]['average_rating']
        
    return jsonify({"title": book.title, "author": book.author, "year": book.year, "isbn": book.isbn, "review_count": reviews_count, "average_score": average})
        



    
     


    
 
    
     
    
    
