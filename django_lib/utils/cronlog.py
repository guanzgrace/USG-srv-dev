import datetime

def fmt(msg):
    return datetime.datetime.utcnow().strftime("%b %d %Y, %H:%M:%S UTC") + "\t" + msg + "\n"
