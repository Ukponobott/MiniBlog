from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/poem_blog'
mongo = PyMongo(app)


app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        posts = mongo.db.posts
        # new_post = request.form["title"], request.form["body"], request.form["author"])
        posts.insert({"title": request.form["title"], "body": request.form["body"], "author": request.form["author"]})
        flash("New Entry Added")
        return redirect(url_for('index'))
    else:
        posts = mongo.db.posts.find()
        return render_template("index.html", posts=posts)


@app.route("/new")
def new_post():
    return render_template("add.html")


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
        return "Welcome " + session["first_name"]


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("first_name", None)
    flash("You are currently logged out")
    return redirect(url_for("index"))


@app.route("/posts/<string:title>")
def show(title):
    posts = mongo.db.posts.find()
    # set the variable "found_post" to an empty string before assigning a value to it later in the condition statement
    found_post = ""
    # loop over all posts to find the one with the title that was passed in in the url
    for post in posts:
        if post["title"] == title:
            found_post = post
        else:
            pass
    return render_template('show.html', post=found_post)


if __name__ == '__main__':
    app.run(debug=True)
