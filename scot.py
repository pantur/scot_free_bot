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
    from random import randint
except ImportError as ie:
    print('ErrorImportingModules', ie)
try:
    from ResConfig import debugFlag as DEBUG, \
        MAX_ERROR_COUNT, SHORT_SLEEP, \
        LONG_SLEEP, MESSAGE, usr, pwd, sec, \
        clid, desc
except ImportError as configError:
    print('UnableToImportConfig', configError)


def connect_to_reddit():
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


def find_violations():
    try:
        for comment in CONN.subreddit('test').stream.comments():
            comment_str = str(comment.body.encode('utf-8').lower())
            if 'scotch-free' in comment_str or 'scotch free' in comment_str:
                if DEBUG:
                    print(comment_str)
                    print('first: ', 'scotch-free' or 'scotch free' in comment_str)
                    print('second: ', 'scotch free' in comment_str)
                    print('third: ', 'scotch-free' in comment_str)
                comment.reply(create_msg(comment.author))
                record_total_violation_count()
                pause_bot(1)
            elif DEBUG:
                print('FindingComments')
    except Exception as ex:
        print('CouldNotPostMessage', ex)


def create_msg(author):
    return MESSAGE.format(str(author))


def pause_bot(len_):
    if len_ == 1:
        sleep_ = randint(1, SHORT_SLEEP)
    elif len_ == 2:
        sleep_ = LONG_SLEEP
    else:
        print('InvalidSleepTime')
        return False

    if DEBUG:
        print('Sleeping for some time...')

    time.sleep(sleep_)

    if DEBUG:
        print('Woke up from sleeping!')

    return True


def record_total_violation_count():
    pass


if __name__ == '__main__':
    ERROR_COUNT = 0
    if DEBUG:
        print('user: ' + usr)
        print('pwd: ' + pwd)
        print('sec: ' + sec)
        print('app: ' + clid)

    try:
        if connect_to_reddit():
            if DEBUG:
                print('Successfully connected to Reddit')
            while True:
                if ERROR_COUNT <= MAX_ERROR_COUNT:
                    try:
                        find_violations()
                    except Exception as e:
                        ERROR_COUNT += 1
                        if DEBUG:
                            print('ERROR_COUNT: ' + str(ERROR_COUNT))
                        print('EncounteredError', e)
                else:
                    if pause_bot(1):
                        print('ResumingOperations')
    except KeyboardInterrupt as ki:
        print('Thanks! See you next time!')
