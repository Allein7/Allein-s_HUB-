from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # keep this secret!

# Folder paths for uploads
UPLOAD_FOLDER = "static/games"
IMAGE_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Hardcoded login (just for you)
USERNAME = "allein"
PASSWORD = "mypassword"

# Projects list
projects = [
    {"title": "Soccer Game ⚽", "desc": "A fun 2-player soccer game with kick, goals, and keepers! 🥅🎵", "file": "SoccerGame.zip", "image": "soccer_game.png"},
    {"title": "Mini Adventure 🎮", "desc": "A mini adventure game to test your skills and reflexes! 🌟", "file": "AnotherGame.zip", "image": "another_game.png"}
]

@app.route("/")
def home():
    logged_in = session.get("logged_in", False)
    return render_template("index.html", logged_in=logged_in)

@app.route("/projects")
def projects_page():
    logged_in = session.get("logged_in", False)
    return render_template("projects.html", projects=projects, logged_in=logged_in)

@app.route("/about")
def about():
    logged_in = session.get("logged_in", False)
    return render_template("about.html", logged_in=logged_in)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("projects_page"))
        else:
            error = "Invalid credentials ❌"
            return render_template("login.html", error=error)
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        file = request.files.get("file")
        image = request.files.get("image")
        if file and image:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            image_path = os.path.join(IMAGE_FOLDER, image.filename)
            file.save(file_path)
            image.save(image_path)
            projects.append({
                "title": title,
                "desc": desc,
                "file": file.filename,
                "image": image.filename
            })
            return redirect(url_for("projects_page"))
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
