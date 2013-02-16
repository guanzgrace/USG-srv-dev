from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from models import Course, Class, Subscription, CoursesList
import log
import json
import urllib2
import traceback

def index(request):
 	return render(request, 'pounce/index.html')
	
def courses(request):
	coursesJson = CoursesList.objects.all()[0].json
	return HttpResponse(coursesJson)
	
def subscribeEmail(request):
	try:
		classNumber = request.GET['classNumber']
		email = request.GET['netid'] + "@princeton.edu"
		log.log("subscribeEmail %s %s" % (classNumber, email))
		theclass = Class.objects.get(number=classNumber)
		subscription = Subscription(address = email, theclass = theclass, type = "EMAIL")
		subscription.save()
		subscription.sendConfirmation()
		return HttpResponse("+<b>Success!</b> You will soon receive an email verifying your subscription for <strong>%s</strong>." % str(theclass))
	except:
		log.log("subscribeEmail ERROR")
		return HttpResponse("-<b>Something went wrong.</b> You are not subscribed for <strong>%s</strong>. If this problem persists, please <a href='mailto:princetonpounce@gmail.com'>contact the developers</a>." % str(theclass))
		
def subscribeText(request):
	try:
		classNumber = request.GET['classNumber']
		phoneNumber = request.GET['number']
		log.log("subscribeText %s %s" % (classNumber, phoneNumber))
		theclass = Class.objects.get(number=classNumber)
		subscription = Subscription(address = phoneNumber, theclass = theclass, type = "TEXT")
		subscription.save()
		subscription.sendConfirmation()
		return HttpResponse("+<b>Success!</b> You will soon receive a text verifying your subscription for <strong>%s</strong>." % str(theclass))
	except:
		return HttpResponse(traceback.format_exc())
		log.log("subscribeEmail ERROR")
		return HttpResponse("-<b>Something went wrong.</b> You are not subscribed for <strong>%s</strong>. If this problem persists, please <a href='mailto:princetonpounce@gmail.com'>contact the developers</a>." % str(theclass))

def reactivate(request, id):
	subscription = Subscription.objects.get(pk=id)
	subscription.active = True
	subscription.save()
	return HttpResponse("You are re-subscribed for %s." % str(subscription.theclass))
	

# 
# def coursedetails(request):
# 	courseid = request.GET['courseid']
# 	html = urllib2.urlopen('https://registrar.princeton.edu/course-offerings/course_details.xml?courseid=%s&term=1134' % courseid).read()
# 	if courseid == '002071':
# 		return HttpResponse(html.replace('Closed', ''))
# 	else:
# 		return HttpResponse(html)
# 	
