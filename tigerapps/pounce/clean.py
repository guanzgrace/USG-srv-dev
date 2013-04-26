import sys,os
sys.path.insert(0,os.path.abspath("/srv/tigerapps"))
import settings
from django.core.management import setup_environ
setup_environ(settings)

from pounce.models import Entry

entries = Entry.objects.all()
past = []
for entry in entries:
	if entry in past:
		print "Deleting", entry.courseNumber, entry.section
		entry.delete()
	else:
		past.append(entry)