from flask import Flask
from datetime import datetime

app = Flask(__name__)

counter = 0


@app.route("/")
def welcome():
    global counter
    counter += 1
    return "Welcome to my Flash Cards application!"


@app.route("/date")
def date():
    global counter
    counter += 1
    return "This page was served at " + str(datetime.now())


@app.route("/count")
def count():
    global counter
    counter += 1
    return "This page was served " + str(counter) + " times"
