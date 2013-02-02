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

def start_servers(django_port, gevent_port):
    os.environ['REAL_TIME_PORT'] = gevent_port
    subprocess.Popen(['manage.py', 'runserver', '0.0.0.0:' + django_port])
    subprocess.Popen(['manage_gevent.py', gevent_port])

if __name__ == '__main__':
    try:
        django_port = int(sys.argv[1])
        gevent_port = int(sys.argv[2])
    except Exception as e:
        print e
        print usage
        sys.exit(1)
    start_servers(str(django_port), str(gevent_port))
