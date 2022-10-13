# We took the beginning 3 lines from server.py to start the __init__ file
# This file now imports flask 
from flask import Flask
app = Flask(__name__)
app.secret_key = "Any string we want here"