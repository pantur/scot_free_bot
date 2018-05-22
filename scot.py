'''  Copyright S.S. Rath, 2018
     All rights reserved.

     This software finds incidences
     of the common malapropism, 
     scotch-free v.s. scot-free,
     on Reddit and notifies users
     of the correct usage.

     Can't let them get away scotch-free!
'''
from __future__ import print_function
try:
    import praw
    import time
except ImportError as ie:
    print('ErrorImportingModules')
try:
    from ResConfig import debugFlag as DEBUG, \
         MAX_ERROR_COUNT, usr, pwd, sec, \
         clid, desc
except ImportError as configError:
    print('UnableToImportConfig')

def connectToReddit():
    global CONN
    try:
        CONN = praw.Reddit(user_agent=desc, \
                               client_id=clid, \
                               client_secret=sec, \
                               username=usr, \
                               password=pwd)
    except Exception as ConnectionError:
        print(ConnectionError)
        return False
    return True

def getTopComments(url):
    top = []
    submission = CONN.submission(url=url)
    submission.comments.replace_more(limit=None)
    for top_level_comment in submission.comments:
        if DEBUG:
            print('-' * 50,) 
            print(top_level_comment.body)
            print('-' * 50,)
        top.append(top_level_comment.body)
    return top

if __name__=='__main__':
    ERROR_COUNT = 0
    if DEBUG:
        print('user: ' + usr)
        print('pwd: ' + pwd)
        print('sec: ' + sec)
        print('app: ' + clid)

    if connectToReddit():
        if DEBUG:
            print('Successfully connected to Reddit')
        while ERROR_COUNT <= MAX_ERROR_COUNT:
            try:
                findViolations()
                getUserName()
                constructMessage()
                postMessage()
                increaseTotalViolationCount()
            except Exception as e:
                ERROR_COUNT += 1
                print('EncounteredError')
                print(e)
        time.sleep(LONG_SLEEP)


