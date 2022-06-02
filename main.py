import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

db.create_all()

all_books = []


@app.route('/')
def home():
    books_in_db = Books.query.all()
    for i in range(len(books_in_db)):
        # print(vars(books_in_db[i])["title"])
        # print(vars(books_in_db[i])["author"])
        # print(vars(books_in_db[i])["rating"])
        # print(type(vars(books_in_db[i])["title"]))
        # print(type(vars(books_in_db[i])["author"]))
        # print(type(vars(books_in_db[i])["rating"]))
        temp_book_dict = {
            "title": vars(books_in_db[i])["title"],
            "author": vars(books_in_db[i])["author"],
            "rating": vars(books_in_db[i])["rating"]
        }
        all_books.append(temp_book_dict)
        print(all_books)
    library = all_books
    return render_template('index.html', library=library)


@app.route("/add")
def add():
    return render_template('add.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    # all_books.append(
    #     {
    #         "title": request.form['bookName'],
    #         "author": request.form['bookAuthor'],
    #         "rating": float(request.form['bookRating']),
    #     }
    # )
    new_book = Books(title=request.form['bookName'], author=request.form['bookAuthor'],
                     rating=float(request.form['bookRating']))
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

