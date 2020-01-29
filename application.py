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

    i = 1
    while i < 80:
        id = str(i)
        res = requests.get("https://api.kuroganehammer.com/api/characters/" + id)
        if res.status_code != 200:
            raise Exception("ERROR: The Get request was unsuccessful, please try again!")

        data = res.json()
        fighterNames.append(data['Name'])
        i += 1
    
    fighterNames.sort()

    return render_template("index.html", fighterNames=fighterNames)

@app.route("/selectedFighter", methods=["POST"])
def selectFighter():
    movelist = {}
    autoCancelledMoves = {}
    selectedFighter = request.form.get("selectedFighter")
    response = requests.get("https://api.kuroganehammer.com/api/characters/name/" + selectedFighter + "/moves?expand=true")
    if response.status_code != 200:
        raise Exception("ERROR: The Get request was unsuccessful, please try again!")
    
    fighterImage = miscInfo(selectedFighter)
    hopAirTime = hopTime(selectedFighter)
    
    autoCancelFrameData = response.json()
    for listItem in autoCancelFrameData:
        movelist[listItem['Name']] = listItem['AutoCancel']
    
    for key in movelist:
        if (movelist[key] == None or movelist[key] == "-"):
            continue
        autoCancelledMoves[key] = movelist[key]
        
    return render_template("character-page.html", autoCancelledMoves=autoCancelledMoves, fighterImage=fighterImage, hopAirTime=hopAirTime)

def miscInfo(characterName):
    miscInfoResponse = requests.get("https://api.kuroganehammer.com/api/characters/name/" + characterName)
    miscData = miscInfoResponse.json()

    characterImage = miscData['ThumbnailUrl'].strip('\"')
    return characterImage

def hopTime(characterName):
    # movementData = {}
    hopTimes = {}
    hopResponse = requests.get("https://api.kuroganehammer.com/api/characters/name/" + characterName + "/movements")
    hopData = hopResponse.json()

    for element in hopData:
        if(element['Name'] != "SH Air Time" and element['Name'] != "FH Air Time"):
            continue
        hopTimes[element['Name']] = element['Value']

    return hopTimes


