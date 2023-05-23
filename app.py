import sqlite3
from flask import Flask, render_template, session, request, url_for, flash, redirect
from flask_session import Session
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = con.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template("post.html", post=post)

@app.route('/searched', methods=["GET", "POST"])
def searched():
    if request.method == "POST":
        keywords = request.form.get("keywords")
        if not keywords:
            flash('Keywords required')
        else:
            post = search(keywords)
            return redirect("search_result.html", post=post)
    else:
        return render_template("search.html")

def search(keywords):
    conn = get_db_connection()
    posts = con.execute("SELECT * FROM posts").fetchall()
    new_dict = {}
    for post in posts:
        new_dict[post["title"]] = 0
        for i in keywords.split(' '):
            if i in post["content"].split(' '):
                new_dict[post['title']] += 1
    result = sorted(new_dict.items())[-1]
    conn.close()
    return result