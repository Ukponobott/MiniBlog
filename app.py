from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
# from flask_bcrypt import
from flask_pymongo import PyMongo
from flask_modus import Modus


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/poem_blog'
mongo = PyMongo(app)
modus = Modus(app)


app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        users = mongo.db.users
        posts = mongo.db.posts
        current_user = users.find_one({"first_name": session["first_name"]})
        # store the post_title in a variable and convert it to lowercase before storing it in the database
        title = request.form["title"]
        title = title.lower()
        posts.insert_one({"title": title,
                          "body": request.form["body"],
                          "author_first_name": current_user["first_name"],
                          "author_last_name": current_user["last_name"]})
        flash("New Entry Added")
        return redirect(url_for('index'))
    else:
        posts = mongo.db.posts.find().sort("title", 1)
        return render_template("index.html", posts=posts)


@app.route("/new")
def new_post():
    if 'first_name' in session:
        return render_template("add.html")
    else:
        flash("Please login to share a post")
        return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = mongo.db.users
        new_user = users.find_one({"email": request.form["email"]})
        if new_user is None:
            users.insert({"first_name": request.form["first_name"], "last_name": request.form["last_name"],
                          "email": request.form["email"], "password": request.form["password"]})
            flash("You have successfully registered, please proceed to SIGN IN")
            return redirect(url_for('login'))
        else:
            flash("User already exists, Please SIGN IN")
            return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("first_name", None)
        users = mongo.db.users
        existing_user = users.find_one({"email": request.form["email"]})
        # find out if user exists or not
        if existing_user is not None:
            if request.form["password"] == existing_user["password"]:
                # check if passwords match to login or stop login
                session["first_name"] = existing_user["first_name"]
                flash("Logged in as " + existing_user["first_name"] + " " + existing_user["last_name"])
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid password, Please try again")
                return redirect(url_for("login"))
        else:
            flash("User does not exist, please register")
            return redirect(url_for("register"))
    else:
        return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "first_name" in session:
        my_posts = mongo.db.posts.find({"author_first_name": session["first_name"]})
        return render_template('dashboard.html', my_posts=my_posts)
    else:
        return redirect(url_for("login"))
# def edit_profile():


@app.route("/logout")
def logout():
    session.pop("first_name", None)
    flash("You are currently logged out")
    return redirect(url_for("index"))


@app.route("/posts/<string:title>", methods=["GET", "PATCH", "DELETE"])
def show(title):
    posts = mongo.db.posts.find()
    # set the variable "found_post" to an empty string before assigning a value to it later in the condition statement
    found_post = ""
    # loop over all posts to find the one with the title that was passed in in the url
    for post in posts:
        if post["title"] == title:
            found_post = post
            if request.method == b'PATCH':
                edit_post = mongo.db.posts
                raw = edit_post.find_one({"title": title})
                new_value = {"$set": {"title": request.form["title"],
                                      "body": request.form["body"]}}
                edit_post.update(raw, new_value)
                return redirect(url_for("index"))
            if request.method == b'DELETE':
                delete_post = mongo.db.posts
                find = delete_post.find_one({"title": title})
                delete_post.delete_one(find)
                return redirect(url_for('index'))
        else:
            pass
    return render_template('show.html', post=found_post)


@app.route('/students/<string:title>/edit')
def edit(title):
    posts = mongo.db.posts.find()
    found_post = ""
    for post in posts:
        if post["title"] == title:
            found_post = post
    return render_template('edit.html', post=found_post)


if __name__ == '__main__':
    app.run(debug=True)
