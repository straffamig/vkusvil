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
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
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
            print(post)
            return render_template("search_result.html", post=post)
    else:
        return render_template("search.html")

def search(keywords):
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    new_dict = {}
    for post in posts:
        temp = 0
        #new_dict[post['title']] = 0
        d = {}
        for i in keywords.split(' '):
            if i in post["content"].split(' '):
                #new_dict[post['title']] += 1
                temp += 1
        d['title'] = post['title']
        d['count'] = temp
        d['post_id'] = post['id']
        d['created'] = post['created']
        if d['count'] > 0:
            new_dict[post['title']] = d
    newdict = {}
    newdict = new_dict.values()
    print(newdict)
    print(new_dict)
    result = dict(sorted(new_dict.items(), key=lambda x : x[1], reverse=True))
    print(result)
    result = result.values()
    conn.close()
    return result