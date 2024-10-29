# Correct indentation for views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User

# from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout  # Make sure logout is imported here
from django.contrib.auth import login, authenticate

# from django.contrib import messages
# from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


def logout_view(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt  # Only if you are sending raw JSON data; otherwise, remove this
def register(request):
    # Handle POST request for registration
    if request.method == "POST":
        try:
            # For form-based POST requests, you should use request.POST instead
            # of request.body.
            # If using raw JSON data, keep this. Otherwise, use request.POST.
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            email = data.get("email")

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {"userName": username, "error": "Already Registered"}, status=400
                )

            # If the username is unique, create the new user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
            )
            # Log in the user after registration
            login(request, user)
            return JsonResponse(
                {"userName": username, "status": "Authenticated"}, status=200
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # If the request is GET (for displaying the form or otherwise)
    # Render your registration form here
    return render(request, "register.html")


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)

    car_make_count = CarMake.objects.count()  # Count the car makes
    car_model_count = CarModel.objects.count()  # Count the car models

    # Print the count of CarMake and CarModel in the server logs
    print(f"CarMake count: {car_make_count}")
    print(f"CarModel count: {car_model_count}")

    if count <= 0:
        initiate()  # Populate data if none exists
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` render list of dealerships, all by default,
# particular state if state is passed


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    # If dealer id has been provided
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            print(response)
            review_detail["sentiment"] = response["sentiment"]
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if not request.user.is_anonymous:
        try:
            # Load the review data from the request body
            data = json.loads(request.body)
            # Call the post_review method to submit the review
            response = post_review(data)
            # Return a success status and message
            return JsonResponse(
                {
                    "status": 200,
                    "message": "Review posted successfully",
                    "response": response,
                }
            )
        except Exception as e:
            return JsonResponse(
                {"status": 401, "message": f"Error in posting review: {e}"}
            )
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
