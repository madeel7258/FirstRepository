from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from pymongo import MongoClient

@api_view(['POST'])
def signup_data(request):
    if request.method == 'POST':
        email = request.data.get('email')
        pharmacy_name = request.data.get('pharmacy_name')
        password = request.data.get('password')

        if not (email and pharmacy_name and password):
            return Response({'message': 'All fields must be provided'}, status=400)

        hashed_password = make_password(password)
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/')
        db = client['pharmacy']
        collection = db['signup_data']

        try:
            # Check if email already exists
            if collection.find_one({'email': email}):
                return Response({'message': 'Email already exists'}, status=409)  # Conflict

            # Create a document to insert
            new_signup = {
                'email': email,
                'pharmacy_name': pharmacy_name,
                'password': hashed_password
            }

            # Insert the document
            collection.insert_one(new_signup)

            # Close the MongoDB connection
            client.close()

            return Response({'message': 'Data saved successfully'}, status=201)
        except Exception as e:
            return Response({'message': 'An error occurred'}, status=500)  # Internal Server Error






@csrf_exempt
def login(request):
    if request.method == 'POST':
        emailPharmacy = request.POST.get('emailPharmacy')
        password = request.POST.get('password')

        if not (emailPharmacy and password):
            return render(request, 'login.html', {'error_message': 'Email/Pharmacy and password are required'})

        # Connect to MongoDB
        client = MongoClient('mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/')
        db = client['pharmacy']
        collection = db['signup_data']

        try:
            user_data = collection.find_one({'$or': [{'email': emailPharmacy}, {'pharmacy_name': emailPharmacy}]})

            if not user_data:
                return render(request, 'login.html', {'error_message': 'User not found'})

            stored_password = user_data['password']
            if not check_password(password, stored_password):
                return render(request, 'login.html', {'error_message': 'Invalid password'})

            # Successful login, redirect to dashboard or another page
            request.session['emailPharmacy'] = emailPharmacy
            return render(request, 'insert.html')  # Change 'dashboard' to the appropriate URL name
        except Exception as e:
            return render(request, 'login.html', {'error_message': 'An error occurred'})

    return render(request, 'login.html')



##===========================


from django.shortcuts import render

def insert_data(request):
    return render(request, 'insert.html')

def show_order(request):
    
    return render(request, 'show_order.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page (adjust the URL name as needed)

