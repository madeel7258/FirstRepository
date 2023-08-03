from django.shortcuts import render, redirect
from pymongo import mongo_client

from .models import user_data  # import model
from django.contrib.auth import logout  # def logout_user(request):
from django.contrib.auth.hashers import make_password  # def user_signup(request):
from django.contrib.auth.hashers import check_password  # def user_login(request)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # def api_user_login(request)
from rest_framework.decorators import api_view  # def api_user_login(request):
from rest_framework_simplejwt.tokens import RefreshToken  # def api_user_login(request):


# Create your views here.
def home_page(request):
    return render(request, 'home_page.html')


##==============================
# this code is signup password save in hash
# ##==============================
from pymongo import MongoClient

def user_signup(request):
    if request.method == 'POST':
        try:
            # MongoDB connection parameters
            mongo_host = 'mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/'
            mongo_db_name = 'User_Data'
            collection_name = 'user_data'

            # Connect to MongoDB
            client = MongoClient(mongo_host)
            db = client[mongo_db_name]
            collection = db[collection_name]

            # Handle the 'name' field
            name = request.POST.get('name')
            if not name or not name.strip():
                return render(request, 'user_signup.html')
            name = name.lower()
            name = name.strip()

            # Handle the 'username' field
            user_name = request.POST.get('username')
            if not user_name or not user_name.strip():
                return render(request, 'user_signup.html')
            user_name = user_name.lower()
            user_name = user_name.strip()

            # Check if the username already exists in the collection
            existing_user = collection.find_one({'user_name': user_name})
            if existing_user:
                error_message = "Username already exists. Please choose a different username."
                return render(request, 'user_signup.html', {'error_message': error_message})

            # Handle the 'email' field
            email = request.POST.get('email')
            if not email or not email.strip():
                return render(request, 'user_signup.html')
            email = email.lower()
            email = email.strip()

            # Handle the 'password' field
            password = request.POST.get('password')
            if not password or not password.strip():
                return render(request, 'user_signup.html')

            # Hash the password using Django's make_password function
            hashed_password = make_password(password)

            # Create a dictionary to store the user data
            user_data = {
                'name': name,
                'user_name': user_name,
                'email': email,
                'password': hashed_password,
                'access_token': None,
            }

            # Insert the user_data into the MongoDB collection
            collection.insert_one(user_data)

            # Close the MongoDB connection
            client.close()

        except Exception as e:
            print("Error:", e)

        return redirect('user_login')  # Replace 'user_login' with the URL name of your login page.

    return render(request, 'user_signup.html')


##=======================================


##================================
# #this code is login password with using hash password
##================================
from pymongo import MongoClient

# Connect to MongoDB
mongo_client = MongoClient('mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/')
db = mongo_client['User_Data']

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # find the user from the user_data collection based on the username

            user_collection = db['user_data']
            user = user_collection.find_one({'user_name': username})

            if user and check_password(password, user['password']):
                # Password matches, user authenticated
                return redirect('home_page')
            else:
                # Invalid password, display login page again with error message
                context = {'error_message': 'Invalid username or password.'}
                return render(request, 'user_login.html', context)

        except Exception as e:
            print("Error:", e)
            # Display login page with error message
            context = {'error_message': 'An error occurred. Please try again later.'}
            return render(request, 'user_login.html', context)

    return render(request, 'user_login.html')



def logout_user(request):
    logout(request)
    return redirect('user_login')  # Replace 'user_login' with the URL name of your login page.


###=======================================
##this is API , request send from the postman to view user_data if JWT authenticate
###========================================

def view_users_api(request):
    if request.method == 'GET':
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/')
        db = client['User_Data']
        user_data_collection = db['user_data']
        # Extract the access token from the Authorization header
        provided_access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

        # Retrieve the user_data object based on the provided access token
        user_data_obj = user_data_collection.find_one({'access_token': provided_access_token})

        if user_data_obj:
            # Access token matches, proceed to return the data
            users_cursor = user_data_collection.find()  # Retrieve all documents from the collection

            # Serialize the user data into JSON format
            user_data_list = []
            for user_obj in users_cursor:
                user_data_list.append({
                    'name': user_obj['name'],
                    'username': user_obj['user_name'],
                    'email': user_obj['email'],
                })

            # Close the MongoDB connection
            client.close()

            # Return the serialized data as a JSON response
            return JsonResponse({'users': user_data_list}, status=200)
        else:
            # Access token doesn't match any user_data object
            client.close()
            return JsonResponse({'message': 'Unauthorized'}, status=401)

    # Return an empty response for unsupported methods
    return JsonResponse({}, status=405)


##=======================================
##this is API , request send from the postman through basic auth
##========================================
#
#
# @csrf_exempt
# def api_user_login(request):
#     if request.method == 'POST':
#         # Get the username and password from the request's Authorization header
#         username, password = get_basic_auth_credentials(request)
#
#         try:
#             # MongoDB connection parameters
#             mongo_host = 'mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/'
#             mongo_db_name = 'User_Data'
#             collection_name = 'user_data'  # Replace with the collection name where user data is stored
#
#             # Connect to MongoDB
#             client = MongoClient(mongo_host)
#             db = client[mongo_db_name]
#             collection = db[collection_name]
#
#             # Retrieve the user from the MongoDB collection based on the username
#             user = collection.find_one({'user_name': username})
#
#             # Check if the user exists and compare the hashed password
#             if user and check_password(password, user['password']):
#                 # Password matches, user authenticated
#                 client.close()
#                 return JsonResponse({'message': 'Congratulations!!! Login Successful'})
#             else:
#                 # Invalid credentials
#                 client.close()
#                 return JsonResponse({'message': 'Invalid credentials'}, status=401)
#
#         except Exception as e:
#             print("Error:", e)
#             # Handle any other exceptions
#             client.close()
#             return JsonResponse({'message': 'Internal server error'}, status=500)
#
#     return JsonResponse({'message': 'This is a POST request endpoint'}, status=400)
#
# import base64
# def get_basic_auth_credentials(request):
#     """
#     Extracts and returns the username and password from the request's Basic Authentication header.
#     """
#     auth_header = request.META.get('HTTP_AUTHORIZATION')
#     if auth_header and auth_header.startswith('Basic '):
#         auth_header = auth_header[len('Basic '):]
#         decoded_auth = base64.b64decode(auth_header).decode('utf-8')
#         return decoded_auth.split(':', 1)
#     return None, None

# =================================================


#
# ##=======================================
# #this is API , request send from the postman and the username and password send from the body part
# ##========================================
#
# import json
# from pymongo import MongoClient
#
# @csrf_exempt
# def api_user_login(request):
#     if request.method == 'POST':
#         # Get the request body as a JSON object
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             password = data.get('password')
#         except json.JSONDecodeError:
#             return JsonResponse({'error_message': 'Invalid JSON data in the request'}, status=400)
#
#         try:
#             # MongoDB connection parameters
#             mongo_host = 'mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/'
#             mongo_db_name = 'User_Data'
#             collection_name = 'user_data'
#
#             # Connect to MongoDB
#             client = MongoClient(mongo_host)
#             db = client[mongo_db_name]
#             collection = db[collection_name]
#
#             # Retrieve the user from the MongoDB collection based on the username
#             user = collection.find_one({'user_name': username})
#
#             # Check if the user exists and compare the hashed password
#             if user and check_password(password, user['password']):
#                 # Password matches, user authenticated
#                 client.close()
#                 return JsonResponse({'message': 'Authentication successful'})
#             else:
#                 # Invalid username or password
#                 client.close()
#                 return JsonResponse({'error_message': 'Invalid username or password.'}, status=401)
#
#         except Exception as e:
#             print("Error:", e)
#             # Handle any other exceptions
#             client.close()
#             return JsonResponse({'error_message': 'Internal server error'}, status=500)
#
#     return JsonResponse({'error_message': 'This is a POST request endpoint'}, status=400)

# ##=================================================


##=================================
##this is API for login user through JWT Auth and access token save in table
##================================
#
# import base64
# import jwt
#
# # Your JWT secret key (keep this secret)
# JWT_SECRET_KEY = ''
#
#
# @csrf_exempt
# def api_user_login(request):
#     if request.method == 'POST':
#         # Get the username and password from the request's Authorization header
#         username, password = get_basic_auth_credentials(request)
#
#         try:
#             # MongoDB connection parameters
#             mongo_host = 'mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/'
#             mongo_db_name = 'User_Data'
#             collection_name = 'user_data'  # Replace with the collection name where user data is stored
#
#             # Connect to MongoDB
#             client = MongoClient(mongo_host)
#             db = client[mongo_db_name]
#             collection = db[collection_name]
#
#             # Retrieve the user from the MongoDB collection based on the username
#             user = collection.find_one({'user_name': username})
#
#             # Check if the user exists and compare the hashed password
#             if user and check_password(password, user['password']):
#                 # Password matches, user authenticated
#
#                 # Generate a JWT access token
#                 access_token = generate_access_token(username)
#                 collection.update_one({'user_name': username}, {'$set': {'access_token': access_token}})
#
#                 # Return the access token in the response
#                 return JsonResponse({'access_token': access_token})
#             else:
#                 # Invalid credentials
#                 client.close()
#                 return JsonResponse({'message': 'Invalid credentials'}, status=401)
#
#         except Exception as e:
#             print("Error:", e)
#             # Handle any other exceptions
#             client.close()
#             return JsonResponse({'message': 'Internal server error'}, status=500)
#
#     return JsonResponse({'message': 'This is a POST request endpoint'}, status=400)
#
#
# def generate_access_token(username):
#     """
#     Generates a JWT access token for the given username.
#     """
#     payload = {
#         'username': username,
#         # You can include additional claims like 'exp' (expiration time), 'iss' (issuer), etc., if needed.
#     }
#     access_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
#     return access_token
#
#
# # The rest of your code remains unchanged...
#
# def get_basic_auth_credentials(request):
#     auth_header = request.META.get('HTTP_AUTHORIZATION')
#     if auth_header and auth_header.startswith('Basic '):
#         auth_header = auth_header[len('Basic '):]
#         decoded_auth = base64.b64decode(auth_header).decode('utf-8')
#         return decoded_auth.split(':', 1)
#     return None, None



##=================================
##this is API for login user through JWT Auth and access token save in table with the expiration t
##================================

import base64
import jwt
from pymongo import MongoClient
from datetime import datetime, timedelta

# Your JWT secret key (keep this secret)
JWT_SECRET_KEY = ''

@csrf_exempt
def api_user_login(request):
    if request.method == 'POST':
        # Get the username and password from the request's Authorization header
        username, password = get_basic_auth_credentials(request)

        try:
            # MongoDB connection parameters
            mongo_host = 'mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/'
            mongo_db_name = 'User_Data'
            collection_name = 'user_data'  # Replace with the collection name where user data is stored

            # Connect to MongoDB
            client = MongoClient(mongo_host)
            db = client[mongo_db_name]
            collection = db[collection_name]

            # Retrieve the user from the MongoDB collection based on the username
            user = collection.find_one({'user_name': username})

            # Check if the user exists and compare the hashed password
            if user and check_password(password, user['password']):
                # Password matches, user authenticated

                # Generate a JWT access token along with its expiration time
                access_token, expiration_time = generate_access_token(username)

                # Save the access token and its expiration time in the MongoDB collection
                collection.update_one({'user_name': username}, {'$set': {'access_token': access_token, 'token_exp': expiration_time}})

                # Return the access token in the response
                return JsonResponse({'access_token': access_token,'expiration_time': expiration_time})
            else:
                # Invalid credentials
                client.close()
                return JsonResponse({'message': 'Invalid credentials'}, status=401)

        except Exception as e:
            print("Error:", e)
            # Handle any other exceptions
            client.close()
            return JsonResponse({'message': 'Internal server error'}, status=500)

    return JsonResponse({'message': 'This is a POST request endpoint'}, status=400)


def generate_access_token(username, expiration_minutes=60):

    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    payload = {
        'username': username,
        'exp': expiration_time,  # Set the expiration time for the token
        # You can include additional claims like 'iss' (issuer), etc., if needed.
    }
    access_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return access_token, expiration_time


# The rest of your code remains unchanged...

def get_basic_auth_credentials(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header and auth_header.startswith('Basic '):
        auth_header = auth_header[len('Basic '):]
        decoded_auth = base64.b64decode(auth_header).decode('utf-8')
        return decoded_auth.split(':', 1)
    return None, None
