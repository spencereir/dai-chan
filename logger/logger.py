import datetime

def log_msg(lvl, msg):
    print('{} : {:%Y-%m-%d %H:%M:%S} : {}'.format(lvl, datetime.datetime.now(), msg))
