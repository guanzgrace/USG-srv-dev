from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from models import *
from emails import sendConfirmEmail, sendNotifyEmail
import urllib2
import datetime

@login_required
def index(request):
	appointments = Appointment.objects.filter(isActive=True).filter(time__gte=datetime.datetime.now()).order_by('time')
	return render_to_response('writetime/index.html', {'appointments' : appointments, 'user' : request.user})

@login_required
def offer(request):
	dates = [datetime.datetime.now() + datetime.timedelta(1) * i for i in range(10)]
	return render_to_response('writetime/offer.html', {'times' : range(9, 22), 'dates' : dates, 'user' : request.user})

@login_required
def accept(request, pk):
	appointment = Appointment.objects.get(pk=pk)
	return render_to_response('writetime/accept.html', {'appointment' : appointment, 'user' : request.user})

@login_required
def submitOffer(request):
	name = request.REQUEST['name']
	netid = request.user.username
	dateString = request.REQUEST['date']
	timeString = request.REQUEST['time']
	(year, month, day) = dateString.split('_')
	time = datetime.datetime(int(year), int(month), int(day), int(timeString))
	appointment = Appointment(name=name, netid=netid, time=time)
	appointment.save()
	sendConfirmEmail(appointment)
	return redirect("/")

@login_required
def submitAccept(request, pk):
	name = request.REQUEST['name']
	netid = request.user.username
	if name and netid:
		appointment = Appointment.objects.get(pk=pk)
		appointment.isActive = False
		appointment.save()
		sendNotifyEmail(appointment, name, netid + "@princeton.edu")
	return redirect("/")

@login_required	
def submitRemove(request, pk):
	appointment = Appointment.objects.get(pk=pk)
	appointment.isActive = False
	appointment.save()
	return redirect("/")
	
@login_required
def authenticate(request):
	return redirect(request.GET['url'] + "?user=" + request.user.username)
	