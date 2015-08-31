# -*- coding: utf-8 -*-
import os
import json
import requests
import time
import re
import codecs
from kitchen.text.converters import getwriter
import sys

def getConfig():
    curPath = os.getcwd()
    data = []
    with open('%s/config.json' % curPath, 'rb') as f:
        data = json.load(f)
    f.close()
    return data

def getUsers(options):
    config = getConfig()
    data = {
        "pagesize":"100",
        "order":"desc",
        "key": config['key'],
        "sort":"reputation",
        "site":"stackoverflow"
        }
    for key in options:
        print key + ': ' + str(options[key])
        data[key] = str(options[key])
    print json.dumps(data)
    headers = {
        "access_token": config['token'],
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding":"gzip"
        }
    jsonRes = requests.get("https://api.stackexchange.com/2.2/users",
        headers=headers,
        data=data
    )
    #print jsonRes.headers
    #print jsonRes.text
    return jsonRes

def recursiveFunc(users, options):
     #regexp = re.compile('^.*?san.*?diego.*?$')
    stashUsers = users
    with open('%s/stackUsers.json' % os.getcwd(), 'rb') as f:
        userList = json.loads(f.read())
    f.close()

    #while users['has_more'] and options['page'] < 10000:
    while users['has_more']:
        try:
            time.sleep(float(users['backoff']) + 1)
        except KeyError:
            pass
        options['page'] += 1
        r = getUsers(options)
        users = json.loads(r.text)
        #print json.dumps(users)
        try:
            if users['error_name'] == 'throttle_violation':
                print 'in if block'
                regexp = re.compile(r"\d+")
                s = re.search(regexp, users['error_message'])
                timeLeft = int(s.group(0))
                print 'sleeping about ' + str(timeLeft / 60) + ' minutes'
                time.sleep((60*5))
                return recursiveFunc(stashUsers, options)
        except:
            pass
        for user in users['items']:
            print user['display_name']
            if 'location' in user:
                print user['location']
                if user['location'].lower().find('san diego') > -1:
                    userList.append(user)
            else:
                print 'no location'
            print '*****'
        with open('%s/stackUsers.json' % os.getcwd(), 'wb') as f:
            json.dump(userList, f, indent=4)
        f.close()
    for key in users['items'][0]:
        print key + ': ' + str(users['items'][0][key])

def unfurlJson(someJson):
    theString = ''
    for key in someJson:
        try:
            theString += str(someJson[key])
        except TypeError as e:
            print e

def jsonToCsv(fileName, separator):
    theStr = ''
    with open('%s/%s.json' % (os.getcwd(), fileName), 'rb') as f:
        theJson = json.loads(f.read())
    f.close()

    methodList =[ 
        {'about_me': 'string'}, 
        {'accept_rate': 'integer'}, 
        {'account_id': 'integer'},
        {'age': 'integer'}, 
        {'answer_count': 'integer'},
        {'badge_counts': 'badge_count'},
        {'creation_date': 'date'},
        {'display_name': 'string'},
        {'down_vote_count': 'integer'},
        {'is_employee': 'boolean'},
        {'last_access_date': 'date'},
        {'last_modified_date': 'date'}, 
        {'link': 'string'}, 
        {'location': 'string'}, 
        {'profile_image': 'string'}, 
        {'question_count': 'integer'},
        {'reputation': 'integer'},
        {'reputation_change_day': 'integer'},
        {'reputation_change_month': 'integer'},
        {'reputation_change_quarter': 'integer'},
        {'reputation_change_week': 'integer'},
        {'reputation_change_year': 'integer'},
        {'timed_penalty_date': 'date'}, 
        {'up_vote_count': 'integer'},
        {'user_id': 'integer'},
        {'user_type': 'string'},
        {'view_count': 'integer'},
        {'website_url': 'string'}
    ] 
    for method in methodList:
        for key in method:
            theStr += str(key) + separator
    theStr += '\n'
    for user in theJson:
        for method in methodList:
            for key in method:
                try:
                    theStr += user[str(key)]
                except TypeError:
                    theStr += str(user[str(key)])
                except KeyError:
                    theStr += 'No ' + str(key)
                except UnicodeError:
                    theStr += 'Unicode Error'
            theStr += separator
        theStr += '\n'
    UTF8Writer = getwriter('utf8')

    with open('%s/%s.csv' % (os.getcwd(), fileName), 'wb') as f:
        f = UTF8Writer(f)
        f.write(theStr)
    f.close()

if __name__ == "__main__":
    jsonToCsv('stackUsers', '^')
    '''
    users = {
        'has_more': True,
        'quota_remaining': 1,
        'backoff': False
    }
    options = {
        "page": 27000
    }
    recursiveFunc(users, options)
    '''
