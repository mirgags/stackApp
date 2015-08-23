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
    data = {
        "pagesize":"100",
        "order":"desc",
        "sort":"reputation",
        "site":"stackoverflow"
        }
    headers = {
        "access_token": config['token'],
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding":"gzip"
        }
    jsonRes = requests.get("https://api.stackexchange.com/2.2/users",
        headers=headers,
        data=data
    )
    print jsonRes.headers
    print jsonRes.text
    return jsonRes

if __name__ == "__main__":
    r = getUsers()
    users = json.loads(r.text)
    for user in users['items']:
        print user['display_name']
        try:
            print user['location']
        except:
            print 'no location'
        print '*****'
