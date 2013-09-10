from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from models import *
from django.core.mail import send_mail
import urllib2
import json
from process import process
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	return render_to_response("sectionswap/index.html")

@login_required
def mustOverwrite(request):
	haveSectionNumber = request.GET['have']

	haveSection = Section.objects.get(number=haveSectionNumber)

	if SwapRequest.objects.filter(netid=request.user.username, have=haveSection).count():
		return HttpResponse("true")
	return HttpResponse("false")

@login_required
def swapRequest(request):
	haveSectionNumber = request.GET['have']
	wantSectionNumbers = request.GET['want'].split(',')
	
	haveSection = Section.objects.get(number=haveSectionNumber)

	if SwapRequest.objects.filter(netid=request.user.username, have=haveSection).count():
		SwapRequest.objects.filter(netid=request.user.username, have=haveSection).delete()

	for wantSectionNumber in wantSectionNumbers:
		wantSection = Section.objects.get(number=wantSectionNumber)
		swap, swapCreated = SwapRequest.objects.get_or_create(netid=request.user.username, have=haveSection, want=wantSection)
		swap.save()
		results = process(swap)
		if results:
			return render_to_response("results.html", {'results' : results})
	return render_to_response("sectionswap/wait.html")

@login_required
def confirmOverwrite(request):
	haveSectionNumber = request.GET['have']
	wantSectionNumbers = request.GET['want'].split(',')
	# TODO: something here
	return render_to_response("sectionswap/overwrite.html")

@login_required
def manage(request):
	swaps = SwapRequest.objects.all()
	# todo: filter by user
	return render_to_response("sectionswap/manage.html", {'swaps' : swaps})

@login_required
def remove(request, pk):
	swap = SwapRequest.objects.get(pk = pk)
	if swap.netid == request.user.username:
		swap.delete()
		return redirect('/manage')
	else:
		return HttpResponse(status=403)

@login_required
def courses(request):
	if len(Cache.objects.all()) == 0:
		courseDicts = []
		for course in Course.objects.all().order_by('code'):
			sectionDicts = []
			sections = Section.objects.filter(course=course).filter(Q(name__startswith="P") | Q(name__startswith="B") | Q(name__startswith="C")).filter(isClosed=True).order_by('name')
			
			if len(sections) < 2:
				continue
			if len(sections.filter(name__startswith='C')) < 2 and len(sections.filter(name__startswith='P')) < 2 and len(sections.filter(name__startswith='B')) < 2:
				continue
			
			for section in sections:
				name = section.name + " (" + section.days + " " + section.time + ")"
				sectionDict = {'number' : section.number, 'name' : name}
				sectionDicts.append(sectionDict)
			code = course.code.split('/')[0].strip() # for demo purposes, keep only the first code synonym
			courseDict = {'code' : code, 'number' : course.number, 'sections' : sectionDicts}
			courseDicts.append(courseDict)
		coursesJson = json.dumps(courseDicts)

		return HttpResponse(coursesJson)

		Cache(json = coursesJson).save()

	cache = Cache.objects.all()[0]
	return HttpResponse(cache.json)
