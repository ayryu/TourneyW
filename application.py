import requests

res = requests.get("https://api.kuroganehammer.com/api/characters/name/ganondorf?game=ultimate")

    if res.status_code != 200:
        raise Exception("ERROR: The Get request was unsuccessful, please try again!")

if __name__ == "__main__":
    main()
