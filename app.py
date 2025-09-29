import json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return ("Hello, World! 🎉 Try visiting /index, /add,"
            "/update, /delete")


@app.route("/index")
def index():
    # add code here to fetch the job posts from a file
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
    print(blog_posts)  # list of dict
    return render_template("index.html", posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
