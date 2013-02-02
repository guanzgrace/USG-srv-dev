import os
import sys
import socket
import subprocess

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

path = '/'.join(__file__.split('/')[:-2])
if path not in sys.path:
    sys.path.append(path)

if socket.gethostname() == 'USGDev':
    import imp
    import monitor
    monitor.start(interval=1.0)

# Start the long-polling gevent server
os.environ['REAL_TIME_PORT'] = '8031'
subprocess.Popen(['manage_gevent.py', '8031'])

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
