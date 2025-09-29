import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World! 🎉 Try visiting /index, /add," "/update, /delete"


@app.route("/index")
def index():
    # add code here to fetch the job posts from a file
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
    print(blog_posts)  # list of dict
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods =["GET", "POST"])
def add():
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        new_id = max([p["id"] for p in blog_posts], default=0) + 1
        blog_posts.append({"id": new_id, "author": author, "title": title, "content": content})
        with open("data/blog.json", "w", encoding="utf-8") as file_object:
            json.dump(blog_posts, file_object, indent=4)
        return redirect (url_for('index'))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
