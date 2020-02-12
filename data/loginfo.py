import json

PATH = "data/json/loginfo.json"

def getloginfo():
    """username, auth_tokenの入ったdictを返す"""
    with open(PATH, "r") as f:
        loginfo = json.load(f)
    return loginfo

def setloginfo(**kwargs):
    """username, auth_tokenのkwargを渡す"""
    with open(PATH, "w") as f:
        json.dump(kwargs, f, indent=4)