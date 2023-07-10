from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello, Flask!'


@app.route("/user/<username>")
def show_user_profile(username):
    return f'User {escape(username)}'


@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f'Post {post_id}'


@app.route("/path/<path:subpath>")
def show_path(subpath):
    return f'Path {escape(subpath)}'
    # http://127.0.0.1:5000/path/%3Cscript%3Ealert(%22bad%22)%3C/script%3E
    # return f'Path {subpath}'


if __name__ == '__main__':
    app.run(debug=True)
