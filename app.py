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


@app.route("/posts")
def posts():
    return "All posts"


if __name__ == '__main__':
    app.run(debug=True)
