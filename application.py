import json
import requests

def main():
    characterNames = []
    res = requests.get("https://api.kuroganehammer.com/api/characters")
    if res.status_code != 200:
        raise Exception("ERROR: The Get request was unsuccessful, please try again!")
        
    data = json.loads(res.text)
    for element in data:
        characterNames.append(element['Name'])

    for name in characterNames:
        print(name)

if __name__ == "__main__":
    main()

#python application.py