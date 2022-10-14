#*******When we are using modularization, we moved the first 3 lines that were in the server file to the __init__ file


# We now changed the first line to below: 
from flask_app import app  
#we are importing app (app = Flask(__name__)) from the flask_app folder. This import, brings Flask back into server.py file

#We need to add in a new line to import our controllers files
from flask_app.controllers import users, posts, memes

#*********We move all @app.routes functions into the controller file

if __name__ == "__main__":
    app.run(debug=True)