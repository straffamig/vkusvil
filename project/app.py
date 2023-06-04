import sqlite3, string, re, urllib, simplejson
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
        keywords = keywords.translate(keywords.maketrans(string.punctuation, ' ', string.punctuation))
        #what if user inputs keywords like this "hey,world,knife"; search will be for heyworldknife; let's replace puncctuation with spaces and after split() in search fuction also do strip()
        if not keywords:
            flash('Keywords required')
        else:
            post = search(keywords)
            print(post)
            return render_template("search_result.html", post=post)
    else:
        return render_template("search.html")

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        link = request.form.get("link")

        if not link:
            flash('Link is required!')
        elif len(link) == 11 or re.search("youtube.com/watch?v=", link):
            if re.search("youtube.com/watch?v=", link):
                link = re.findall("\S+?\Sv=+", link)
            try:
                url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % link
                json = simplejson.load(urllib.urlopen(url))
                author = json['entry']['author'][0]['name']
                title = json['entry']['title']['$t']
                content = YouTubeTranscriptApi.get_transcript(link[0],
                                            languages=['ru'])
                content = content['text']
                conn = get_db_connection()
                conn.execute('INSERT INTO videos (title, link, content, author) VALUES (?, ?, ?, ?)',
                            (title, link, content, author))
                conn.commit()
                conn.close()
                flash("Post added!")
                return redirect(url_for('index'))
            except:
                flash("It's supposed to be a YT link :)")

    return render_template("create.html")

def search(keywords):
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    new_dict = {}
    post = set(posts['content'])
    temp = 0
    temp_start = 0
    #new_dict[post['title']] = 0
    d = {}
    for post in posts:
        for i in keywords.split(' '):
            if i in post["content['text']"].lower().split(' ').strip():
                #new_dict[post['title']] += 1
                temp += 1
                temp_start = post["content['start']"]
        d['title'] = post['title']
        d['start'] = temp_start
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