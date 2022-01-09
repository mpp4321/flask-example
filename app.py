from flask import Flask, render_template, request, make_response, redirect
import hashlib
import redis

app = Flask(__name__)
redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route("/")
def home_route():
    return render_template("home.html")

@app.route("/login", methods = ["POST"])
def login_route():
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    if username == None or password == None:
        return render_template("home.html", error = "Please enter a username and password.")

    password_hashed = hashlib.sha256(password.encode()).hexdigest()

    if not redis.exists(username):
        redis.set(username, password_hashed)
        return render_template('registered.html', username=username)

    if redis.get(username) == password_hashed:
        str_res = render_template("success.html")
        resp = make_response(str_res)
        resp.set_cookie('username', username)
        resp.set_cookie('password', password_hashed)
        return resp
    else:
        return render_template("failure.html")

@app.route('/loggedin')
def logged_in():
    uname = request.cookies.get('username', None)
    phash = request.cookies.get('password', None)
    if uname != None and redis.get(uname) == phash:
        return render_template("loggedin.html", username=uname)
    else:
        return redirect('/', code=401)
