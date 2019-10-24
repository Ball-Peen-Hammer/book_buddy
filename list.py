import os
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    search = "mid"
    books = Library.query.filter(Library.title.ilike("%" + search + "%")).limit(10)
    for book in books:
        print(book.title)
    

if __name__ == "__main__":
    with app.app_context():
        main()