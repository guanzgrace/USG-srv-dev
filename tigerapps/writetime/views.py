from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from models import *
from emails import sendEmail
import urllib2
import datetime

def index(request):
	appointments = Appointment.objects.filter(isActive=True).filter(time__gte=datetime.datetime.now()).order_by('time')
	return render_to_response('writetime/index.html', {'appointments' : appointments})

def offer(request):
	dates = [datetime.datetime.now() + datetime.timedelta(1) * i for i in range(10)]
	return render_to_response('writetime/offer.html', {'times' : range(9, 22), 'dates' : dates})

def accept(request, pk):
	appointment = Appointment.objects.get(pk=pk)
	return render_to_response('writetime/accept.html', {'appointment' : appointment})

def submitOffer(request):
	name = request.REQUEST['name']
	email = request.REQUEST['email']
	dateString = request.REQUEST['date']
	timeString = request.REQUEST['time']
	(year, month, day) = dateString.split('_')
	time = datetime.datetime(int(year), int(month), int(day), int(timeString))
	appointment = Appointment(name=name, email=email, time=time)
	appointment.save()
	return redirect("/")

def submitAccept(request, pk):
	name = request.REQUEST['name']
	email = request.REQUEST['email']
	if name and email:
		appointment = Appointment.objects.get(pk=pk)
		appointment.isActive = False
		appointment.save()
		sendEmail(appointment, name, email)
	return redirect("/")
	
def submitRemove(request, pk):
	appointment = Appointment.objects.get(pk=pk)
	appointment.isActive = False
	appointment.save()
	return redirect("/")