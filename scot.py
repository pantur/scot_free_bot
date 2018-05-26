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
    print(ie)
try:
    from ResConfig import debugFlag as DEBUG, \
        MAX_ERROR_COUNT, SHORT_SLEEP, \
        LONG_SLEEP, usr, pwd, sec, \
        clid, desc
except ImportError as configError:
    print('UnableToImportConfig')
    print(configError)


def connectToReddit():
    global CONN
    try:
        CONN = praw.Reddit(user_agent=desc,
                           client_id=clid,
                           client_secret=sec,
                           username=usr,
                           password=pwd)
    except Exception as ConnectionError:
        print(ConnectionError)
        return False
    return True


def findViolations():
    for comment in CONN.subreddit('test').stream.comments():
        if 'scotch-free' in str(comment.body.encode('utf-8')):
            print(comment.body.encode('utf-8'))


def pauseBot(len_):
    if DEBUG:
        print('Sleeping for some time...')
    
    if len_ == 1:
        time.sleep(SHORT_SLEEP)
    elif len_ == 2:
        time.sleep(LONG_SLEEP)
    else:
        print('InvalidSleepTime')
        return False
    
    if DEBUG:
        print('Woke up from sleeping!')

    return True


def recordTotalViolationCount():
    pass


if __name__ == '__main__':
    ERROR_COUNT = 0
    if DEBUG:
        print('user: ' + usr)
        print('pwd: ' + pwd)
        print('sec: ' + sec)
        print('app: ' + clid)

    try:
        if connectToReddit():
            if DEBUG:
                print('Successfully connected to Reddit')
            while True:
                if ERROR_COUNT <= MAX_ERROR_COUNT:
                    try:
                        findViolations()
                        recordTotalViolationCount()
                    except Exception as e:
                        ERROR_COUNT += 1
                        if DEBUG:
                            print('ERROR_COUNT: ' + str(ERROR_COUNT))
                        print('EncounteredError')
                        print(e)
                else:
                    if pauseBot(1):
                        print('ResumingOperations')
    except KeyboardInterrupt as ki:
        print('Thanks! See you next time!')
