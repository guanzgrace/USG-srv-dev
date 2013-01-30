#!/usr/bin/python
# This script runs the long-polling server instance

import os, sys, time, subprocess
from gevent.pywsgi import WSGIServer
import django.core.handlers.wsgi

DEFAULT_PORT = 8031
PIDFILE = '/srv/logs/gevent_server_%d.pid'
TRIES = 5


path = '/'.join(__file__.split('/')[:-1])
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tigerapps.settings'
os.environ['IS_REAL_TIME_SERVER'] = 'TRUE'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = DEFAULT_PORT

    pidfile = PIDFILE % port

    # Kill the old server if need be
    if os.path.exists(pidfile):
        f = open(pidfile)
        oldpid = int(f.read())
        code = subprocess.call(['kill', '-15', str(oldpid)])
        f.close()

    # Write the new pid
    pid = os.getpid()
    f = open(pidfile, 'w')
    f.write(str(pid))
    f.close()

    application = django.core.handlers.wsgi.WSGIHandler()

    print 'Long-polling gevent server on %d...' % port
    for i in range(0, TRIES):
        try:
            WSGIServer(('', port), application).serve_forever()
        except Exception as e:
            print e
            time.sleep(.01)
    print 'Long-polling gevent server not running'

