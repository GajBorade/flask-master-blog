import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


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


@app.route("/add", methods=["GET", "POST"])
def add():
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        new_id = max([p["id"] for p in blog_posts], default=0) + 1
        blog_posts.append(
            {"id": new_id, "author": author, "title": title, "content": content}
        )
        with open("data/blog.json", "w", encoding="utf-8") as file_object:
            json.dump(blog_posts, file_object, indent=4)
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete(post_id):
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
        # Filtering or rebuilding a list with exclusions
        new_blog_posts = []
        for old_post in blog_posts:
            if old_post["id"] != post_id:
                new_blog_posts.append(old_post)

    with open("data/blog.json", "w", encoding="utf-8") as file_object:
        json.dump(new_blog_posts, file_object, indent=4)
        flash("Post deleted successfully!", "success")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
