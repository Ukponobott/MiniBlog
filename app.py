from flask import Flask, redirect, render_template, request
from poem import Poem
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/poem_blog'
mongo = PyMongo(app)


@app.route("/", methods=["GET", "POST"])
def index():
    posts = mongo.db.posts
    if request.method == "POST":
        new_post = Poem(request.form["title"], request.form["body"], request.form["author"])
        posts.insert(new_post)
    else:
        return render_template("index.html", posts=posts)


@app.route("/new")
def new_post():
    return render_template("add.html")


@app.route("/register")
def register():
    return "Register to Post a Poem"


@app.route("/login")
def login():
    return "Login to your Account"


@app.route("/posts/<string>/title")
def posts(title):
    return "Single post"


if __name__ == '__main__':
    app.run(debug=True)
