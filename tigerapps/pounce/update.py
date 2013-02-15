import princetonpounce.settings
from django.core.management import setup_environ
setup_environ(princetonpounce.settings)

from pounce.models import Course, Class, Subscription, Entry, CoursesList
import pounce.log as log
from django.core.mail import EmailMessage
import urllib2
from bs4 import BeautifulSoup

def updateCourse(course):
	log.log("Updating %s" % str(course))
		
 	url = "https://registrar.princeton.edu/course-offerings/course_details.xml?courseid={}&term=1134".format(course.number)
# 	url = "http://princetonpounce.com/course-offerings/course_details.xml?courseid={}&term=1134".format(course.number)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	
	rows = soup.find_all('tr')[1:]
	for row in rows:
			fields = row.find_all('td')
			
			classNumber = fields[0].get_text().strip()
			if not classNumber:
				continue
				
			theclass, created = Class.objects.get_or_create(number=classNumber, course=course)
			theclass.title = fields[1].get_text().strip()
			theclass.time = fields[2].get_text().strip().replace("\n", "")
			theclass.days = fields[3].get_text().strip().replace("\n", "")
			raw = fields[5].get_text().replace("\n","").replace(" ","")
			sindex = raw.find("Enrolled:")
			eindex = raw.find("Limit:")
			theclass.enroll = int(raw[sindex+9:eindex])
			theclass.max = int(raw[eindex+6:] or 1000)
			
			isClosed = fields[6].get_text().strip() == "Closed"
			if not isClosed:
				log.log("Class %s is now open!" % str(classNumber))
				for subscription in Subscription.objects.filter(theclass=theclass, active=True):
					log.log("Sending subscription %s." % str(subscription))
					subscription.sendNotification()
					subscription.active = False
					subscription.save()
					
			theclass.isClosed = isClosed
			
			theclass.save()
				
def scrape():	
	# Gets the main page of all classes
	url = "https://registrar.princeton.edu/course-offerings/search_results.xml?term=1134"
# 	url = 'http://princetonpounce.com/static/course_offerings_test.html'

	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)

	# Iterates through all courses
	rows = soup.find_all('tr')[1:]
	for row in rows:
			fields = row.find_all('td')

			if (fields[10].get_text().strip() == "Cancelled"):
				continue

			courseNumber = fields[1].a['href'][28:34]
			section = fields[4].get_text().strip()
			enroll = int(fields[8].get_text().strip())
			closed = fields[10].get_text().strip() == "Closed"
			
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
 	
 	list = CoursesList.objects.all()[0]
 	list.cache()
 	
log.log('Running update.py')
 
if (len(CoursesList.objects.all()) == 0):
	CoursesList().save()

scrape()