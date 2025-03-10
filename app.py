from flask import Flask, request, render_template, redirect, url_for, make_response
import jwt
import datetime
import os

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")

DUMMY_USERS = {
    os.getenv("DUMMY_USER_1"): os.getenv("DUMMY_PASS_1"),
}

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")
FLAG = os.getenv("FLAG")

def generate_jwt():
    payload = {
        "user": ADMIN_USER,
        "password": ADMIN_PASS,
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in DUMMY_USERS and DUMMY_USERS[username] == password:
            response = make_response(redirect(url_for("capture_jwt")))
            response.set_cookie("seatf-jwt", generate_jwt())
            return response
        elif username == ADMIN_USER and password == ADMIN_PASS:
            response = make_response(redirect(url_for("flag")))
            return response
        return "Invalid credentials!", 403
    return render_template("login.html")

@app.route("/capture")
def capture_jwt():
    return render_template("image.html")

@app.route("/flag")
def flag():
    return render_template("flag.html", flag=FLAG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
