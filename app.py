import os
import json
import requests

def getConfig():
    curPath = os.getcwd()
    data = []
    with open('%s/config.json' % curPath, 'rb') as f:
        data = json.load(f)
    f.close()
    return data

def getUsers():
    config = getConfig()
    data = {}
    headers = {
        "Contant-Type": "application/x-www-form-urlencoded",
        }
    jsonRes = requests.post("http://stackoverflow.com/")

if __name__ == "__main__":
    print json.dumps(getConfig());
