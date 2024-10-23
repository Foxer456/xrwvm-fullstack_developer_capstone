# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv



load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
# Add code for get requests to back end
    # Prepare URL parameters from kwargs
    params = ""
    if kwargs:
        params = "&".join([f"{key}={value}" for key, value in kwargs.items()])

    # Construct the request URL
    request_url = f"{backend_url}/{endpoint}?{params}"
    print(f"GET from {request_url}")

    try:
        # Send the GET request
        response = requests.get(request_url)
        
        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        if response.status_code == 200:
            return response.json()  # Gibt ein Dictionary zurück
        else:
            print(f"Failed to analyze sentiment: {response.status_code}")
            return {"sentiment": "unknown"}  # Gibt ein Dictionary mit einem Standardwert zurück
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"sentiment": "unknown"}  # Gibt ein Dictionary mit einem Standardwert zurück



def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return {"status": "error", "message": "Network exception occurred"}

