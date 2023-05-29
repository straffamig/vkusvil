import sqlite3, string, re
from flask import Flask, render_template, session, request, url_for, flash, redirect
from flask_session import Session
from werkzeug.exceptions import abort
from youtube_transcript_api import YouTubeTranscriptApi

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
        keywords = keywords.lower()
        keywords = keywords.translate(keywords.maketrans('', '', string.punctuation))
        if not keywords:
            flash('Keywords required')
        else:
            post = search(keywords)
            print(post)
            return render_template("search_result.html", post=post)
    else:
        return render_template("search.html")

@app.route('/create', methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        link = request.form("link")

        if not link:
            flash('Link is required!')
        elif not re.search("https://www.youtube.com/watch?v=", link) or re.search("youtube.com/watch?v=", link):
            flash('Provide a youtube link!')
        else:
            link = re.findall("\S+?\Sv=+", link)
            if link.lendth > 1:
                flash("Supposed to enter one link!")
                return redirect(url_for("index"))
            content = YouTubeTranscriptApi.get_transcript(link,
                                          languages=['ru'])
            content = content['text']
            conn = get_db_connection()
            conn.execute('INSERT INTO videos (link, content) VALUES (?, ?)',
                         (link, content))
            conn.commit()
            conn.close()
            flash("Post added!")
            return redirect(url_for('index'))

    return render_template("create.html")

def search(keywords):
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    new_dict = {}
    for post in posts:
        temp = 0
        #new_dict[post['title']] = 0
        d = {}
        for i in keywords.split(' '):
            if i in post["content"].lower().split(' '):
                #new_dict[post['title']] += 1
                temp += 1
        d['title'] = post['title']
        d['count'] = temp
        d['post_id'] = post['id']
        d['created'] = post['created']
        new_dict[temp] = d
    result = dict(sorted(new_dict.items(), key=lambda x : x[0], reverse=True))
    final_result = result[0]
    print(result)
    print(final_result)
    conn.close()
    return final_result