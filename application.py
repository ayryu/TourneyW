import os

from flask import Flask, render_template, request, session
from flask_session import Session
from models import *
import json
import requests

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    fighterNames = []
    res = requests.get("https://api.kuroganehammer.com/api/characters")
    if res.status_code != 200:
        raise Exception("ERROR: The Get request was unsuccessful, please try again!")
        
    data = json.loads(res.text)
    for element in data:
        fighterNames.append(element['Name'])

    for name in fighterNames:
        print(name)

    return render_template("index.html", fighterNames=fighterNames)

@app.route("/<str:selectedFighter>")
def selectFighter():
    movelist = {}
    selectedFighter = request.form.get("selectedFighter")
    response = requests.get("https://api.kuroganehammer.com/api/characters/name/" + selectedFighter + "/moves?expand=true")
    if response.status_code != 200:
        raise Exception("ERROR: The Get request was unsuccessful, please try again!")
    
    frameData = json.loads(response.text)
    #for listItem in frameData:
        #movelist.append(listItem["AutoCancel"])

    return render_template("character-page.html")


#python application.py