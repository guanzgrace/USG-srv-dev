import sys,os
sys.path.insert(0,os.path.abspath("/srv/tigerapps"))
import settings
from django.core.management import setup_environ
setup_environ(settings)

from pounce.models import Course, Class, Subscription, Entry, CoursesList
import pounce.log as log
from django.core.mail import EmailMessage
import urllib2
from bs4 import BeautifulSoup
import twitter
from update import updateCourse, clean, TERM

def scrape():	
	clean()

	# Gets the main page of all classes
	url = "https://registrar.princeton.edu/course-offerings/search_results.xml?term={}".format(TERM)

	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)

	# Iterates through all courses
	rows = soup.find_all('tr')[1:]
	for row in rows:
			try:
				fields = row.find_all('td')

				if (fields[10].get_text().strip() == "Cancelled"):
					continue

				courseNumber = fields[1].a['href'][28:34]
				section = fields[4].get_text().strip()
				enroll = int(fields[8].get_text().strip())
				closed = fields[10].get_text().strip() == "Closed" # or Closed Closed? 
							
				entry, created = Entry.objects.get_or_create(courseNumber=courseNumber, section=section)
	 			if created or enroll != entry.totalEnroll or closed != entry.totalClosed:
					entry.totalEnroll = enroll
					entry.totalClosed = closed
					entry.save()

					course, created = Course.objects.get_or_create(number=courseNumber)
					course.code = ' / '.join([code.strip().replace("  ", " ") for code in fields[1].text.split('\n \n')])
					course.title = fields[2].text.strip()
					course.save()
	 				updateCourse(course)
	 		except Exception:
	 			pass
 	
 	list = CoursesList.objects.all()[0]
 	list.cache()
 	
log.log('Running updatenew.py')
 
if (len(CoursesList.objects.all()) == 0):
	CoursesList().save()

scrape()
