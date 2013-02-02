from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from utils.dsml import gdi
from django.contrib.auth.decorators import login_required, user_passes_test
from models import *
from views import check_undergraduate
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django import forms
import json
import sys,os
import traceback

from real_time_avail import start_sim, stop_sim, check_avail
from real_time_queue import check, edit
    
@login_required
def update_queue(request, drawid):
    user = check_undergraduate(request.user.username)
    if not user:
        return HttpResponse('forbidden')
    draw = Draw.objects.get(pk=drawid)
    qlist = json.loads(request.POST['queue'])
    queue = user.queues.filter(draw=draw)[0]
    if not queue:
        return HttpResponse('no queue')
    try:
        return edit(user, queue, qlist, draw)
    except Exception as e:
        return HttpResponse(e)

# Ajax for displaying this user's queue
@login_required
def get_queue(request, drawid, timestamp = 0):
    user = check_undergraduate(request.user.username)
    timestamp = int(timestamp)
    if not user:
        return HttpResponse('no user')
    try:
        draw = Draw.objects.get(pk=drawid)
        queue = user.queues.get(draw=draw)
    except Exception as e:
        return HttpResponse(traceback.format_exc(2) + str(draw))
    try:
        return check(user, queue, timestamp)
    except Exception as e:
        return HttpResponse(traceback.format_exc(2))
    
def start_simulation(request, delay, size=1):
    delay = int(delay)
    size = int(size)
    return start_sim(delay, size)

def stop_simulation(request):
    return stop_sim()

def check_availability(request, timestamp):
    return check_avail(int(timestamp))
