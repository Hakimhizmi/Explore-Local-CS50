from flask import Flask, flash, redirect, render_template, request, session, jsonify
import requests

app = Flask(__name__)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/explore")
def explore():
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
            return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run()
