from flask import Flask, render_template, request
import redis

app = Flask(__name__)
redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route("/")
def home_route():
    return render_template("home.html")

@app.route( "/login", methods = ["POST"] )
def login_route():
    username = request.form['username']
    password = request.form['password']

    if not redis.exists(username):
        redis.set(username, password)
        return render_template('registered.html', username=username)

    if redis.get(username) == password:
        return render_template("success.html")
    else:
        return render_template("failure.html")
