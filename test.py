import requests

def search_best_place(api_key, location, search_type):
    endpoint = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "term": search_type,  # Type of place you want to search (e.g., "restaurant", "hotel")
        "location": location,
        "sort_by": "rating",  # Sort by rating to get the best-rated place
       "limit": 1    # Limit to one result (the best-rated place)
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200:
            businesses = data.get("businesses")
            if businesses:
                for i in businesses :
                    print(i)
                    print("\n"*2)
            else:
                print("No results found.")
        else:
            print(f"Error: Unable to fetch data from the Yelp API. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Replace 'YOUR_YELP_API_KEY' with your actual Yelp Fusion API key
yelp_api_key = '9oEzAgNdDzgATHf95S5AuP8LgptVmuCMgHVFapmeKGCasp_8oae4WsqbU4ZhySS__TTiH-kvp1E_DhJvxMfVhH6YvKy5bxcvnHWAXcxrT4gzyEpYpBXJqUhqOFsZZXYx'
location = "paris"  # You can specify the location you want to search in
search_type = "gym"  # Type of place you want to search for

search_best_place(yelp_api_key, location, search_type)


