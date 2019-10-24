from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()




class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_reviews = db.relationship("UserReviews", uselist=False, back_populates="user", lazy=True)


class UserReviews(db.Model):
    __tablename__ = "user_reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_score = db.Column(db.Integer, nullable=False)
    user_review = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="user_reviews")
    
    def __init__(self, book_id, user_id, user_score, user_review):

        self.book_id = book_id
        self.user_id = user_id
        self.user_score = user_score
        self.user_review =user_review

class Library(db.Model):
    __tablename__ = "library"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)


   


    









    

 
