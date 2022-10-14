from flask_app import app
from flask import Flask, render_template, redirect, request, session
# We need to import the requests package that we downloaded (pipenv install requests)
import requests
# We need to import jsonify to run JavaScript.
from flask import jsonify

# API step 5 (create route to use api data) ->controllers file --
@app.route('/meme_data')
def getMemedata():
    # jsonify will serialize data into JSON (JacaScript object notation) format.
    r = requests.get("https://meme-api.herokuapp.com/gimme")
    # we must keep in line with JSON format.
    # requests has a method to convert the data coming back into JSON.
    return jsonify( r.json() )
    # Return jsonify because a JavaScript file is making the request but a python file is handling the request
    # We cant give python data to a JavaScript file