from flask import Flask, redirect, render_template, request, url_for
# from poem import Poem
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/poem_blog'
mongo = PyMongo(app)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        posts = mongo.db.posts
        # new_post = request.form["title"], request.form["body"], request.form["author"])
        posts.insert({"title": request.form["title"], "body": request.form["body"], "author": request.form["author"]})
        return redirect(url_for('index'))
    else:
        posts = mongo.db.posts.find()
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
    view = mongo.db.posts.find_one({"title": title})
    return render_template('show.html', post=view)



if __name__ == '__main__':
    app.run(debug=True)
