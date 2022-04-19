import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Connect to the database
MONGODB_HOST = 'mongodb+srv://admin:admin@cluster0.8xlzy.mongodb.net/SuperVoices?retryWrites=true&w=majority'