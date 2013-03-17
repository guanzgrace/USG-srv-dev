import datetime

DIR = "/srv/logs/"

def log(fname, msg):
    f = open(DIR + fname + ".log", "a")
    f.write(str(datetime.datetime.now()) + "\t" + msg)
    f.close()
