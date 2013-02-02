#!/usr/bin/python
"""
This script is a helper script for running both the Django dev server and the
gevent real-time long-polling server with specified ports.

Both stdout and stderr are inherited from this process.
"""

usage="""Usage:
manage_all.py <Django dev server port> <gevent server port>
"""
import os, sys, subprocess
import signal
import time

def run_servers(django_port, gevent_port):
    os.environ['REAL_TIME_PORT'] = gevent_port
    django = subprocess.Popen(
        ['manage.py', 'runserver', '0.0.0.0:' + django_port])
    gevent = subprocess.Popen(['manage_gevent.py', gevent_port])

    def clean_up(signum, frame):
        print 'Recieved signal %d. Cleaning up...' % signum
        gevent.terminate()
        django.terminate()
        time.sleep(1)
        if gevent.poll() is None:
            gevent.kill()
        if django.poll() is None:
            django.kill()
        print 'Both servers stopped.'
        sys.exit(0)

    signal.signal(signal.SIGINT, clean_up)
    signal.pause()

if __name__ == '__main__':
    try:
        django_port = int(sys.argv[1])
        gevent_port = int(sys.argv[2])
    except Exception as e:
        print e
        print usage
        sys.exit(1)
    run_servers(str(django_port), str(gevent_port))
