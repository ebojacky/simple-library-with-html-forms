from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
OPTION: USING SQLite

db = sqlite3.Connection("books_database.db")
cursor = db.cursor()

table_creattion_sql = "CREATE TABLE books (id INTEGER PRIMARY KEY," \
    "title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)"

cursor.execute(table_creattion_sql)

cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()
"""

# USING SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


"""
# CREATE DATABASE
print("about to create db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)
print("db created")

# CREATE TABLE
print("about to create table")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()
print("table created")

all_books = db.session.query(Book).all()
print(all_books)

# CREATE RECORD
print("about to insert record")
new_book = Book(title="Harry Potter", author="J. K. Rowling", rating=9.3)
db.session.add(new_book)
db.session.commit()
print("record inserted")

all_books = db.session.query(Book).all()
print(all_books)
"""


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        book = {
            "title": request.form["bookname"],
            "author": request.form["bookauthor"],
            "rating": request.form["bookrating"]
        }
        # all_books.append(my_dict)

        new_book = Book(title=book["title"], author=book["author"], rating=book["rating"])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route('/edit_rating/<book_id>', methods=["GET", "POST"])
def edit_rating(book_id):

    if request.method == "POST":
        book_to_update = Book.query.filter_by(id=book_id).first()
        book_to_update.rating = request.form["bookrating"]
        db.session.commit()

        return redirect(url_for('home'))

    book = Book.query.filter_by(id=book_id).first()
    return render_template("edit_rating.html", book=book)


@app.route('/delete/<book_id>')
def delete(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
