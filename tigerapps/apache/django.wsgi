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
PORT = '8031'
os.environ['REAL_TIME_PORT'] = PORT
subprocess.Popen([os.path.join(path, 'manage_gevent.py'), PORT])

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
