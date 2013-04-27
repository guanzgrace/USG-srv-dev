import sys,os
sys.path.insert(0,os.path.abspath("/srv/tigerapps"))
import settings
from django.core.management import setup_environ
setup_environ(settings)

from pounce.models import Entry

def contains(list, entry):
	for e in list:
		if entry.courseNumber == e.courseNumber and entry.section == e.section:
			return True
	return False

entries = Entry.objects.all()
past = []
for entry in entries:
	if contains(past, entry):
		print "Deleting", entry.courseNumber, entry.section
		entry.delete()
	else:
		past.append(entry)