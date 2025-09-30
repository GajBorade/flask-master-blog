import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def hello_world():
    """Return a simple greeting message with hints for available routes."""
    return "Hello, World! 🎉 Try visiting /index, /add," "/update, /delete"


@app.route("/index")
def index():
    """Load all blog posts from JSON file and render the index page."""
    # Fetch the job posts from a file
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
    print(blog_posts)  # list of dict
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Handle adding a new blog post; supports form display (GET) and submission (POST)."""
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
    """Delete a blog post by its unique ID and flash a confirmation message."""
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
        # Filtering or rebuilding a list with exclusions
        new_blog_posts = []
        found = False # Flag to check if post exists
        for old_post in blog_posts:
            if old_post["id"] != post_id:
                new_blog_posts.append(old_post)
            else:
                found = True

    with open("data/blog.json", "w", encoding="utf-8") as file_object:
        json.dump(new_blog_posts, file_object, indent=4)

    if found:
        flash("Post deleted successfully!", "success")
    else:
        flash("Post not found, try again later.", "error")
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Update a blog post by its unique ID and flash a confirmation message."""
    with open("data/blog.json", "r", encoding="utf-8") as file_object:
        blog_posts = json.load(file_object)
    # fetch post by id
    post = None
    for p in blog_posts:
        if p["id"] == post_id:
            post = p
            break

    if post is None:
        flash("Post not found!", "error")
        return "Post not found!", 404

    if request.method == "POST":
        # update fields from form
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip().title()
        content = request.form.get("content", "").strip()

        # apply defaults if empty and flash messages
        if not title:
            title = "Undecided"
            flash("Default title applied: 'Undecided'", "info")
        if not author:
            author = "Anonymous"
            flash("Default author applied: 'Anonymous'", "info")
        if not content:
            content = "Writers block"
            flash("Default content applied: 'Writers block'", "info")

        new_id = max([p["id"] for p in blog_posts], default=0) + 1

        # append new post with defaults applied
        blog_posts.append({
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        })

        # Write back to JSON / Update JSON
        with open("data/blog.json", "w", encoding="utf-8") as file_object:
            json.dump(blog_posts, file_object, indent=4)

        # Flash update message
        flash("Post updated successfully!", "success")
        return redirect(url_for("index"))
    # Else, it's a GET request
    # So display the update.html page
    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
