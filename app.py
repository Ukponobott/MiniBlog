from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to Poem Paradise"


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
