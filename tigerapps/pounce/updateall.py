import sys,os
sys.path.insert(0,os.path.abspath("/srv/tigerapps"))
import settings
from django.core.management import setup_environ
setup_environ(settings)

from pounce.models import Course, Class, Subscription, Entry, CoursesList
import pounce.log as log
from update import updateCourse, clean


log.log('Running updateall.py')

clean()

for course in Course.objects.all():
    try:
	   updateCourse(course)
    except Exception:
        print "Error updating course %s" % course.title

list = CoursesList.objects.all()[0]
list.cache()