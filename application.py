import os

from flask import Flask, render_template, request, session
from flask_session import Session
import json
import requests

app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

@app.route("/")
def index():
    fighterNames = []
    res = requests.get("https://api.kuroganehammer.com/api/characters")
    if res.status_code != 200:
        raise Exception("ERROR: The Get request was unsuccessful, please try again!")

    data = res.json()
    for element in data:
        fighterNames.append(element['Name'])

    return render_template("index.html", fighterNames=fighterNames)

@app.route("/selectedFighter", methods=["POST"])
def selectFighter():
    movelist = {}
    autoCancelledMoves = {} #key=move name value=autocancelvalue
    selectedFighter = request.form.get("selectedFighter")
    response = requests.get("https://api.kuroganehammer.com/api/characters/name/" + selectedFighter + "/moves?expand=true")
    if response.status_code != 200:
        raise Exception("ERROR: The Get request was unsuccessful, please try again!")
    
    frameData = response.json()
    for listItem in frameData:
        movelist[listItem['Name']] = listItem['AutoCancel']
    
    for key in movelist:
        if (movelist[key] == None or movelist[key] == "-"):
            continue
        autoCancelledMoves[key] = movelist[key]
        
    return render_template("character-page.html", autoCancelledMoves=autoCancelledMoves)

