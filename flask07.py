from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite.///users.sqlite3'
app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes = 5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Intger, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        # Check if the user input is empty before proceeding
        if not user:
            flash("Please enter your name", "error")
            return redirect(url_for("login"))

        session.permanent = True
        session["user"] = user
        flash("Login Succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session ["user"]

        if request.method == "POST":
            email = request.form ["email"]
            session ["email"] = email
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session ["email"]

        return render_template("user.html", email = email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)