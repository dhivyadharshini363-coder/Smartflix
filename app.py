from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------------- INIT DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie TEXT NOT NULL,
            name TEXT NOT NULL,
            rating REAL NOT NULL,
            comment TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ADD REVIEW ----------------
@app.route("/add-review", methods=["POST"])
def add_review():
    data = request.get_json()
    name = data.get("name")
    movie = data.get("movie")
    rating = data.get("rating")
    comment = data.get("comment")

    if not all([name, movie, rating, comment]):
        return jsonify({"message": "All fields are required"}), 400

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('INSERT INTO reviews(movie, name, rating, comment) VALUES(?,?,?,?)',
              (movie, name, float(rating), comment))
    conn.commit()
    conn.close()

    return jsonify({"message": "Review added successfully!"})

# ---------------- GET REVIEWS ----------------
@app.route("/get-reviews/<movie_title>")
def get_reviews(movie_title):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('SELECT name, rating, comment FROM reviews WHERE movie=?', (movie_title,))
    rows = c.fetchall()
    conn.close()
    reviews = [{"name": r[0], "rating": r[1], "comment": r[2]} for r in rows]
    return jsonify(reviews)

# ---------------- TEST ROUTE ----------------
@app.route("/test")
def test():
    return jsonify({"status": "Flask is running successfully"})

if __name__ == "__main__":
    app.run(debug=True)