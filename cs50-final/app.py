import os

from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_session import Session

# Control layer — routing only
import modules.auth_module as auth_module
import modules.user_module as user_module

app = Flask(__name__)
app.config["SECRET_KEY"] = "329847034299467236894"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)


@app.route("/", methods=["GET", "POST"])
def login():
    """Login page"""
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        status = request.form.get("status")
        if status is None or int(status) < 1:
            return redirect("/apology?code=400&message=Invalid status selected")

        user_info = auth_module.authenticate_user(email, password, status)

        if user_info["success"]:
            session["email"] = email
            session["authority"] = status
            return redirect("/home")
        else:
            return redirect(f"/apology?code=403&message={user_info['message']}")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        status = request.form.get("status")
        password = request.form.get("password")

        user_info = auth_module.authenticate_user(email, password, status)
        if user_info["success"]:
            return redirect("/apology?code=400&message=An account with that email already exists")
        if status is None or int(status) < 1:
            return redirect("/apology?code=400&message=Invalid status selected")
        if status > 1:
            profile = auth_module.set_profile(email, status)
            if not profile["success"]:
                return redirect(f"/apology?code=500&message={profile['message']}")
            result = auth_module.register_admin(email, password, status)
            if not result["success"]:
                return redirect(f"/apology?code=500&message={result['message']}")
            return redirect("/login")
        else:
            profile = auth_module.set_profile(email, status)
            if not profile["success"]:
                return redirect(f"/apology?code=500&message={profile['message']}")
            result = auth_module.register_user(email, password, status)
            if not result["success"]:
                return redirect(f"/apology?code=500&message={result['message']}")
            session["email"] = email
            session["authority"] = status
            return redirect("/home")

    else:
        return render_template("register.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/home", methods=["GET", "POST"])
def home():
    if "email" not in session:
        return redirect("/")

    if request.method == "GET":
        profile = user_module.get_profile(session["email"])
        if not profile["success"]:
            return redirect(f"/apology?code=404&message={profile['message']}")
        return render_template("home.html", profile=profile["data"])

    if request.method == "POST":
        name_id = request.form.get("subject_id")
        result = user_module.choose_subject(session["email"], name_id)

        return redirect("/home")
    

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "email" not in session:
        return redirect("/")

    if request.method == "GET":
        profile = user_module.get_profile(session["email"])
        if not profile["success"]:
            return redirect(f"/apology?code=404&message={profile['message']}")
        return render_template("profile.html", profile=profile["data"])

    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        result = user_module.update_profile(session["email"], {"name": name, "email": email})
        if not result["success"]:
            return redirect(f"/apology?code=500&message={result['message']}")
        session["email"] = email
        return redirect("/profile")
    

@app.route("/subjects", methods=["GET", "POST"])
def subjects():
    if "email" not in session:
        return redirect("/")
    if request.method=="POST":
        q = request.args.get("q")
        year = request.args.get("year") 
        semester = request.args.get("semester")

        subjects = user_module.search_subjects(q, year, semester)
        if not subjects["success"]:
            subjects = {"data": []}  ##only for testing

        return render_template("subjects.html", subjects=subjects["data"])
    else:
        subjects = user_module.search_subjects(None, None, None)
        if not subjects["success"]:
            subjects = {"data": []}  ##only for testing

        return render_template("subjects.html", subjects=subjects["data"])


@app.route("/apology")
def apology():
    code = request.args.get("code", 400)
    message = request.args.get("message", "An unexpected error occurred")
    return render_template("apology.html", code=code, message=message)


if __name__ == "__main__":
    app.run(debug=True)