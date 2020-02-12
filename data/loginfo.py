import json

PATH = "data/json/loginfo.json"

def getloginfo():
    with open(PATH, "r") as f:
        loginfo = json.load(f)
    return loginfo

def setloginfo(**kwargs):
    with open(PATH, "w") as f:
        json.dump(kwargs, f, indent=4)