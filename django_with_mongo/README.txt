To integrate Django with MongoDB via the "djongo" package, begin by creating a new Django project and installing "djongo" using pip, using pymongo version --3.12.3
pip install pymongo==3.12.3
pip install djongo

 In your project's settings, configure the database settings to employ MongoDB as the backend, specifying details such as the database name, MongoDB host.
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA':False,

        'NAME': 'User_Data',  # Replace 'mydatabase' with your desired database name
        'CLIENT': {
            'host': 'mongodb+srv://adeel:system@system.rj37wzv.mongodb.net/',  # Replace with your MongoDB Atlas connection string
        }
    }
}

 Establish a new Django app and define models within its "models.py" file.
Initiate migrations to create MongoDB collections, and then proceed to craft views within your app,
python manage.py makemigrations
python manage.py migrate

Finally, by starting the Django development server, you can validate the successful connection between Django and MongoDB, confirming that your application leverages MongoDB as its database backend.
