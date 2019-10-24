import csv
import os


from flask import Flask, render_template, request
from models import *



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    b = open("books.csv")
    reader = csv.reader(b)
    for isbn, title, author, year in reader:
        book = Library(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
    db.session.commit()
  

if __name__ == "__main__":
    with app.app_context():
        main()

