from django.shortcuts import render, redirect
from .models import user_data       # import model
from django.contrib.auth import logout   # def logout_user(request):
from django.contrib.auth.hashers import make_password  # def user_signup(request):
from django.contrib.auth.hashers import check_password    # def user_login(request)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt    # def api_user_login(request)
from rest_framework.decorators import api_view    # def api_user_login(request):
from rest_framework_simplejwt.tokens import RefreshToken    # def api_user_login(request):

# Create your views here.
def home_page(request):
    return render(request, 'home_page.html')


# #==============this code is signup simply password without hash
# def user_signup(request):
#     if request.method == 'POST':
#         # Extract the data from the POST request
#         name = request.POST.get('name')
#         user_name = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#
#         # Create a new instance of the user_data model and save the data
#         signup = user_data(name=name, user_name=user_name, email=email, password=password)
#         signup.save()
#
#         # Optionally, you can redirect the user to a success page or do any other necessary action.
#         return redirect('user_login')  # Replace 'success_page' with the URL name of your success page.
#
#     return render(request, 'user_signup.html')  # Replace 'signup_form.html' with the name of your signup form template.
# #=========================================



##==============================
#this code is signup password save in hash
# ##==============================

def user_signup(request):
    if request.method == 'POST':
        try:
            # Handle the 'name' field
            name = request.POST.get('name')
            if not name or not name.strip():  # Check if the name field is missing or empty
                return render(request, 'user_signup.html')
            name = name.lower()   # Convert the name to lowercase as required
            name = name.strip()
            user_name = request.POST.get('username')
            if not user_name or not user_name.strip():  # Check if the username field is missing or empty
                return render(request, 'user_signup.html')
            user_name = user_name.lower()            # Convert the username to lowercase as required
            user_name = user_name.strip()
            # Handle the 'email' field
            email = request.POST.get('email')
            if not email or not email.strip():  # Check if the email field is missing or empty
                return render(request, 'user_signup.html')
            # Convert the email to lowercase as required
            email = email.lower()
            email = email.strip()
            # Handle the 'password' field
            password = request.POST.get('password')
            if not password or not password.strip():  # Check if the password field is missing or empty
                return render(request, 'user_signup.html')

            # Hash the password using Django's make_password function
            hashed_password = make_password(password)

            # Create a new instance of the user_data model with the hashed password
            signup = user_data(name=name, user_name=user_name, email=email, password=hashed_password)
            signup.save()
        except Exception as e:
            print("Error:", e)
        return redirect('user_login')  # Replace 'user_login' with the URL name of your login page.

    return render(request, 'user_signup.html')  # Replace 'user_signup.html' with the name of your signup form template

##=======================================

# #==============this code is login password simply without using hash password
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # Check if a user with the given username and password exists in the user_data table
#         try:
#             user = user_data.objects.get(user_name=username, password=password)
#             # If user exists, redirect to the home page
#             return redirect('home_page')  # Replace 'home' with the URL name of your home page.
#
#         except user_data.DoesNotExist:
#             # If the user does not exist or the password is incorrect, display the login page again with an error message.
#             context = {'error_message': 'Invalid username or password.'}
#             return render(request, 'user_login.html', context)
#
#     return render(request, 'user_login.html')

#=====================================



##================================
# #this code is login password with using hash password
##================================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Retrieve the user from the custom user_data table based on the username
            user = user_data.objects.get(user_name=username)

            # Manually check the password against the hashed password stored in the database
            if check_password(password, user.password):
                print(password)
                # Password matches, user authenticated
                # Perform login manually (optional if you are not using Django's built-in authentication)
                # login(request, user)
                return redirect('home_page')  # Replace 'home_page' with the URL name of your home page.
            else:
                # Invalid password, display login page again with error message
                context = {'error_message': 'Invalid username or password.'}
                return render(request, 'user_login.html', context)

        except user_data.DoesNotExist:
            # User not found, display login page again with error message
            context = {'error_message': 'Invalid username or password.'}
            return render(request, 'user_login.html', context)

    return render(request, 'user_login.html')


def logout_user(request):
    logout(request)
    return redirect('user_login')  # Replace 'user_login' with the URL name of your login page.


###=======================================
##this is API , request send from the postman to view user_Data if JWT authenticate
###========================================
def view_users_api(request):
    if request.method == 'GET':
        # Extract the access token from the Authorization header
        provided_access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

        # Retrieve the user_data object based on the provided access token
        try:
            user_data_obj = user_data.objects.get(access_token=provided_access_token)

            # Access token matches, proceed to return the data
            users = user_data.objects.all()

            # Serialize the user data into JSON format
            user_data_list = []
            for user_obj in users:
                user_data_list.append({
                    'name': user_obj.name,
                    'username': user_obj.user_name,
                    'email': user_obj.email,
                })

            # Return the serialized data as a JSON response
            return JsonResponse({'users': user_data_list})

        except user_data.DoesNotExist:
            # Access token doesn't match any user_data object
            return JsonResponse({'message': 'Unauthorized'}, status=401)

    # Return an empty response for unsupported methods
    return JsonResponse({}, status=405)

##=======================================
#this is API , request send from the postman through basic auth
##========================================


#
# @csrf_exempt
# def api_user_login(request):
#     if request.method == 'POST':
#         # Get the username and password from the request's Authorization header
#         username, password = get_basic_auth_credentials(request)
#
#         try:
#             # Retrieve the user from the custom user_data table based on the username
#             user = user_data.objects.get(user_name=username)
#
#             # Manually check the password against the hashed password stored in the database
#             if check_password(password, user.password):
#                 # Password matches, user authenticated
#                 return JsonResponse({'message': 'Congratulations!!! Login Successful'})
#             else:
#                 # Invalid password
#                 return JsonResponse({'message': 'Invalid credentials'}, status=401)
#
#         except user_data.DoesNotExist:
#             # User not found
#             return JsonResponse({'message': 'Invalid credentials'}, status=401)
#
#     return JsonResponse({'message': 'This is a POST request endpoint'}, status=400)
#
# @login_required
# def api_protected_endpoint(request):
#     # This is an example of a protected endpoint that requires authentication
#     # The `login_required` decorator ensures that only authenticated users can access it.
#     return JsonResponse({'message': 'This is a protected endpoint'})
#
# import base64
#
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

# #=================================================


#
# ##=======================================
# #this is API , request send from the postman and the username and password send from the body part
# ##========================================
#
#
# from django.contrib.auth.decorators import login_required
# import json
#
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
#             # Retrieve the user from the custom user_data table based on the username
#             user = user_data.objects.get(user_name=username)
#
#             # Manually check the password against the hashed password stored in the database
#             if check_password(password, user.password):
#                 # Password matches, user authenticated
#                 return JsonResponse({'message': 'Authentication successful'})
#             else:
#                 # Invalid password
#                 return JsonResponse({'error_message': 'Invalid username or password.'}, status=401)
#
#         except user_data.DoesNotExist:
#             # User not found
#             return JsonResponse({'error_message': 'Invalid username or password.'}, status=401)
#
#     return JsonResponse({'error_message': 'This is a POST request endpoint'}, status=400)
#
# @login_required
# def api_protected_endpoint(request):
#     # This is an example of a protected endpoint that requires authentication
#     # The `login_required` decorator ensures that only authenticated users can access it.
#     return JsonResponse({'message': 'This is a protected endpoint'})
# ##=================================================


##=================================
##this is API for login user through JWT Auth and access token save in table
##================================
@api_view(['POST'])
def api_user_login(request):
    if request.method == 'POST':
        # Get the username and password from the request's Authorization header
        username, password = get_basic_auth_credentials(request)

        try:
            # Retrieve the user from the custom user_data table based on the username
            user = user_data.objects.get(user_name=username)

            # Manually check the password against the hashed password stored in the database
            if check_password(password, user.password):
                # Generate the JWT token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Save the access token in the user_data model
                user.access_token = access_token
                user.save()

                # Return the token in the response
                return JsonResponse({'Congratulations login successful!!!  access_token': access_token})

            else:
                # Invalid password
                return JsonResponse({'message': 'Invalid credentials'}, status=401)

        except user_data.DoesNotExist:
            # User not found
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'message': 'This is a POST request endpoint'}, status=400)


@login_required
def api_protected_endpoint(request):
    # This is an example of a protected endpoint that requires authentication
    # The `login_required` decorator ensures that only authenticated users can access it.
    return JsonResponse({'message': 'This is a protected endpoint'})

import base64

def get_basic_auth_credentials(request):
    """
    Extracts and returns the username and password from the request's Basic Authentication header.
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header and auth_header.startswith('Basic '):
        auth_header = auth_header[len('Basic '):]
        decoded_auth = base64.b64decode(auth_header).decode('utf-8')
        return decoded_auth.split(':', 1)
    return None, None
