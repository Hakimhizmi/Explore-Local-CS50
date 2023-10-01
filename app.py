from flask import Flask, flash, redirect, render_template, request, session, jsonify
import requests
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///saved.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


@app.route("/")
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/explore" , methods=["GET", "POST"])
def explore():
    if request.method == "GET":
        location = request.args.get('city')
        search_type = request.args.get('search_type')

        yelp_api_key = "9oEzAgNdDzgATHf95S5AuP8LgptVmuCMgHVFapmeKGCasp_8oae4WsqbU4ZhySS__TTiH-kvp1E_DhJvxMfVhH6YvKy5bxcvnHWAXcxrT4gzyEpYpBXJqUhqOFsZZXYx"

        endpoint = "https://api.yelp.com/v3/businesses/search"
        headers = {"Authorization": f"Bearer {yelp_api_key}"}
        params = {
            "term": search_type,  # Use 'term' for the search term
            "location": location,  # Use 'location' for the location
            "sort_by": "rating",
            "limit": 10,
        }

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            data = response.json()

            if response.status_code == 200:
                businesses = data.get("businesses")
                if businesses:
                    return render_template("explore.html" , data=businesses , location = location , search_type = search_type)
                else:
                    return render_template("explore.html" , data=[] , location = location , search_type = search_type)
            else:
                return render_template("explore.html" , data=[] , location = location , search_type = search_type)
        except Exception as e:
            return apology(str(e), 403)
    else :
        url = request.form.get("url")
        image_url = request.form.get("image_url")
        rating = request.form.get("rating")
        name = request.form.get("name")
        display_address = request.form.get("display_address[]")
        display_address = " ".join(display_address)
        categorie = request.form.get("categories")
        try :
            db.execute("INSERT INTO saved (url, image_url, rating, name, display_address, categories , user_id) VALUES (?, ?, ?, ?, ?, ? , ?)", url, image_url, rating,name,display_address,categorie ,session["user_id"])
            return redirect('/saved')

        except Exception as e:
            return apology(str(e), 403)

@app.route("/saved", methods=["GET", "POST"])
def Saved():
    if request.method == "GET":
        data = db.execute("SELECT * FROM saved where user_id = (?)",session["user_id"])
        return render_template("saved.html" , data=data )

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password_hashed"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET" :
        return render_template("register.html")
    else :
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirme = request.form.get("confirmation")
        checkuser = db.execute("select username from users where username = ?",username)

        if checkuser or password != password_confirme :
            return apology("username Already Taken and/or password dont match!", 400)
        else :
            db.execute("insert into users (username,password_hashed) values (?,?)", username , generate_password_hash(password,method='pbkdf2', salt_length=16))
            return redirect("/login")    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


